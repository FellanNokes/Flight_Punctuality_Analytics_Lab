import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import dlt
import requests
from dotenv import load_dotenv

# Empty the staging_staging schema after each merge load
dlt.config["load.truncate_staging_dataset"] = True

BASE_URL = "https://api.swedavia.se/flightinfo/v2"

# Swedavia airports (section 1.3.1 in the docs)
AIRPORTS = ["ARN", "BMA", "GOT", "MMX", "LLA", "UME", "OSD", "VBY", "RNB", "KRN"]

# The API only accepts dates 2 days back (tested, the docs say 7)
DAYS_BACK = 2


def _get_headers():
    load_dotenv()
    api_key = os.getenv("SWEDAVIA_API_KEY")
    if api_key is None:
        raise RuntimeError("SWEDAVIA_API_KEY not found, check your .env")

    return {
        "Accept": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }


def _get_flights(airport, flight_type, flight_date, headers):
    url = f"{BASE_URL}/{airport}/{flight_type}/{flight_date.isoformat()}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()  # check for http errors
    return response.json()


def _dates_to_fetch_utc(days_back):
    """The last days_back days plus today, in UTC, oldest first.
    With days_back=2 this gives [today-2, today-1, today]."""
    today = datetime.now(timezone.utc).date()
    return [today - timedelta(days=d) for d in range(days_back, -1, -1)]


def _fetch_flights(flight_type, days_back=DAYS_BACK):
    """Yield all flights of one type (arrivals or departures) for all airports and dates."""
    headers = _get_headers()

    for flight_date in _dates_to_fetch_utc(days_back):
        print(f"Fetching {flight_type} for {flight_date}")

        for airport in AIRPORTS:
            try:
                data = _get_flights(airport, flight_type, flight_date, headers)
            except requests.HTTPError as e:
                print(f"  {airport}: failed ({e}) {e.response.text[:300]}")
                continue

            # Docs use PascalCase, the JSON is usually camelCase, so handle both
            flights = data.get("flights") or data.get("Flights") or []
            print(f"  {airport}: {len(flights)} flights")

            for flight in flights:
                yield {
                    **flight,
                    "airport": airport,
                    "flight_type": flight_type,
                    "flight_date": flight_date.isoformat(),
                    # Unique per flight per airport per day, used to merge overlapping runs
                    "flight_key": f"{flight_type}_{airport}_{flight.get('flightId')}_{flight_date.isoformat()}",
                }


@dlt.resource(name="arrivals", write_disposition="merge", primary_key="flight_key")
def arrivals_resource():
    yield from _fetch_flights("arrivals")


@dlt.resource(name="departures", write_disposition="merge", primary_key="flight_key")
def departures_resource():
    yield from _fetch_flights("departures")


# Dagster only works with dlt sources, not resources
@dlt.source
def flights_source():
    return [arrivals_resource(), departures_resource()]


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="swedavia_flights", destination="snowflake", dataset_name="staging"
    )

    load_info = pipeline.run(flights_source())
    print(load_info)