import pandas as pd
import dlt
import requests
from io import StringIO
from bs4 import BeautifulSoup



wikipedia_url = "https://en.wikipedia.org/wiki"

@dlt.resource(name="airports", write_disposition="replace")
def get_airports():
    airport_url = f"{wikipedia_url}/List_of_international_airports_by_country"

    headers = {"User-Agent": "airport-codes-scraper/0.1 (https://github.com/FellanNokes/Flight_Punctuality_Analytics_Lab)"}
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

    yield df_airports

@dlt.resource(name="airlines", write_disposition="replace")
def get_airlines():
    airlines_url = f"{wikipedia_url}/List_of_airline_codes"

    headers = {"User-Agent": "airline-codes-scraper/0.1 (https://github.com/FellanNokes/Flight_Punctuality_Analytics_Lab)"}
    resp = requests.get(airlines_url, headers=headers, timeout=30)
    resp.raise_for_status()
    tables = pd.read_html(StringIO(resp.text))

    df_airlines = tables[0]

    yield df_airlines

@dlt.source
def wikipedia_source():
    return [get_airports(), get_airlines()]