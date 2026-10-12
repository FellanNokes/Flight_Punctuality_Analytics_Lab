import pandas as pd
import dlt
import requests
from io import StringIO
from bs4 import BeautifulSoup



wikipedia_url = "https://en.wikipedia.org/wiki"

@dlt.resource(write_deposition="merge")
def get_airports():
    airport_url = f"{wikipedia_url}/List_of_international_airports_by_country"

    headers = {"User-Agent": "airport-codes-scraper/0.1 (your@email.com)"}
    airport_resp = requests.get(airport_url, headers=headers, timeout=30)
    airport_resp.raise_for_status()

    soup = BeautifulSoup(airport_resp.text, "lxml")

    frames = []

    for table in soup.select("table.wikitable"):
        df = pd.read_html(StringIO(str(table)))[0]

        df["country"] = table.find_previous(["h3", "h4"]).get_text(strip=True)
        df["continent"] = table.find_previous("h2").get_text(strip=True)

        frames.append(df)

    df_airports = pd.concat(frames, ignore_index=True)
    df_airports = df_airports[["Location", "Airport", "IATA Code", "ICAO Code", "country", "continent"]]

    yield df_airports


def run_pipelines():
    pipeline_airports = dlt.pipeline(
        pipeline_name="wikipedia_airports",
        destination="snowflake",
        dataset_name="staging"
    )


    data = get_airports()
    load_info = pipeline_airports.run(data, table_name="airports")
    print(load_info)








airlines_url = f"{wikipedia_url}/List_of_airline_codes"

