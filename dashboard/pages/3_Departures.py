import streamlit as st
from connect_data_warehouse import query_mart
from pathlib import Path

ASSETS_PATH = Path(__file__).parents[1] / "assets"

# Departures overview
def layout_departures_overview():
    df = query_mart("basic_departures")
    st.image(ASSETS_PATH / "img" / "Departures_v1.png", width='stretch')

if __name__ == "__main__":
    layout_departures_overview()