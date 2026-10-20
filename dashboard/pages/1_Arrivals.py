import streamlit as st
from connect_data_warehouse import query_mart
from pathlib import Path
import matplotlib.pyplot as plt

ASSETS_PATH = Path(__file__).parents[1] / "assets"

@st.cache_data
def load_arrivals():
    return query_mart("basic_arrivals")

# Arrivals overview
def layout_arrivals_overview():
    df = load_arrivals()

    st.image(ASSETS_PATH / "img" / "Arrivals_v1.png", width='stretch')

    st.info(body="The Arrivals Overview provides a comprehensive snapshot of flight arrivals, highlighting key metrics and trends.")

    airport_options = ["All airports"] + df["AIRPORT_NAME"].unique().tolist()

    selected_airport = st.selectbox(
        label="Choose swedish airport",
        options=airport_options
    )

    if selected_airport == "All airports":
        filtered_df = df["AIRPORT_NAME"]
    else:
        filtered_df = df[df["AIRPORT_NAME"] == selected_airport]

    filtered_df = df[df["AIRPORT_NAME"] == selected_airport]

    cols = st.columns(4)

    with cols[0]:
        st.metric(
            label="Amount of arrivals",
            value=filtered_df["AMOUNT_OF_FLIGHTS"].sum()
        )
    with cols[1]:
        st.metric(
            label="Delayed arrivals",
            value=filtered_df["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"].sum()
        )
    with cols[2]:
        st.metric(
            label="Delayed arrivals (%)",
            value=filtered_df["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"].sum()/filtered_df["AMOUNT_OF_FLIGHTS"].sum()
        )
    with cols[3]:
        st.metric(
            label="On Time Arrivals",
            value=filtered_df["AMOUNT_NOT_DELAYED_ARRIVAL"].sum()
        )

    pie_df = filtered_df[filtered_df["ARRIVAL_DELAYED_TIME"] != "On Time"]

    counts = pie_df["ARRIVAL_DELAYED_TIME"].value_counts()
    arrival_delayed_time_options = pie_df["ARRIVAL_DELAYED_TIME"].unique().tolist()

    if counts.empty:
        st.warning("No delayed flights for the selected airport.")
    else:
        fig, ax = plt.subplots()
        pie = ax.pie(counts, labels=arrival_delayed_time_options)
        ax.pie_label(pie, counts)
        st.pyplot(fig)

if __name__ == "__main__":
    layout_arrivals_overview()
