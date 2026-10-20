import os

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# The marts the dashboard is allowed to read (table names in the mart schema). If you create a new mart you need to add it here
MARTS = ["arrivals_filter_mart", "departures_filter_mart"]

def _connect():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )

def query_mart(mart: str) -> pd.DataFrame:
    """Return all rows from one of the marts in MARTS."""
    # Only know mart names reach the SQL, so no user input ends up in the query
    if mart not in MARTS:
        raise ValueError(f"Uknown mart {mart}, choose one of {MARTS}")

    with _connect() as conn:
        return pd.read_sql(f"SELECT * FROM {mart}", conn)