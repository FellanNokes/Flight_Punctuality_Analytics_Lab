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
        filtered_df = df
    else:
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

    cols2 = st.columns(2)

    with cols2[0]:

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


    with cols2[1]:
        st.info(body="The Arrivals Overview provides a comprehensive snapshot of flight arrivals, highlighting key metrics and trends.")


    #top_5_df = df.nlargest(5, "AMOUNT_DELAYED_FLIGHTS_ARRIVALS").set_index(df["AIRLINE_NAME"])
    #top_5_df = df.sort_values(by="AMOUNT_DELAYED_FLIGHTS_ARRIVALS", ascending=False).head(5)

    top_5_df = (
        df.groupby("AIRLINE_NAME", as_index=False)["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"]
        .sum()
        .nlargest(5, "AMOUNT_DELAYED_FLIGHTS_ARRIVALS")
    )
  
    st.bar_chart(
        top_5_df,
        x="AIRLINE_NAME",
        y="AMOUNT_DELAYED_FLIGHTS_ARRIVALS",
        sort="-AMOUNT_DELAYED_FLIGHTS_ARRIVALS"       
        )

if __name__ == "__main__":
    layout_arrivals_overview()
