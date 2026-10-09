import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
 
import dlt
import requests
from dotenv import load_dotenv
 
BASE_URL = "https://api.swedavia.se/flightinfo/v2"
 
# Swedavia airports (section 1.3.1 in the docs)
AIRPORTS = ["ARN", "BMA", "GOT", "MMX", "LLA", "UME", "OSD", "VBY", "RNB", "KRN"]
FLIGHT_TYPES = ("arrivals", "departures")
 
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
 
 
def _days_back_utc(n_days):
    """Last n_days in UTC, oldest first. The API expects UTC dates."""
    today = datetime.now(timezone.utc).date()
    return [today - timedelta(days=d) for d in range(n_days, 0, -1)]
 
 
@dlt.resource(write_disposition="merge", primary_key="flight_key")
def flights_resource(flight_type, n_days=DAYS_BACK):
    headers = _get_headers()
 
    for flight_date in _days_back_utc(n_days):
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
 
 
def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="swedavia_flights", destination="snowflake", dataset_name="staging"
    )
 
    for flight_type in FLIGHT_TYPES:
        load_info = pipeline.run(flights_resource(flight_type), table_name=flight_type)
        print(load_info)
 
 
if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
 
    run_pipeline()