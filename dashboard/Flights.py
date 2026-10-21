# Homepage
import streamlit as st
from pathlib import Path
from helper import clickable_image

# Konfigurera sökvägen till assets/img baserat på var Flights.py ligger
# Justera denna beroende på din mappstruktur (här utgår vi från att Flights.py ligger i root)
ASSETS_PATH = Path(__file__).parent / "assets" / "img"

def layout_home_page():
    # Sidans titel och introduktionstext
    st.title("Välkommen till Flight Punctuality Analytics")
    st.info(body="""
    **Departures Overview**

    This dashboard provides a comprehensive snapshot of flight departures across Swedish airports, focusing on punctuality and delays. 
    Click on the links below to dive deeper into each respective area.
    """)

    st.divider()

    # Skapa en 2x2 grid för bilderna och länkarna
    col1, col2 = st.columns(2)

    with col1:
            # Länkmålet ska motsvara hur Streamlit döper sidorna i webbadressen. 
            # Till exempel om filen heter "1_Arrivals.py" blir länken "Arrivals".
            clickable_image(ASSETS_PATH / "start_arrivals_basic.png", "Arrivals")

    with col2:
        clickable_image(ASSETS_PATH / "start_arrivals_details.png", "Arrivals_Details")

    st.write("") # Skapar lite extra vertikalt avstånd mellan raderna

    col3, col4 = st.columns(2)

    with col3:
        clickable_image(ASSETS_PATH / "start_departures_basic.png", "Departures")

    with col4:
        clickable_image(ASSETS_PATH / "start_departures_details.png", "Departures_Details")

if __name__ == "__main__":
    st.set_page_config(page_title="Flight Punctuality Analytics", layout="wide")
    layout_home_page()