import streamlit as st
from connect_data_warehouse import query_mart
from pathlib import Path
from utils.charts import pie_chart_late
from utils.filters import pick_airport, pick_date, apply_filters

ASSETS_PATH = Path(__file__).parents[1] / "assets"

@st.cache_data
def load_arrivals():
    return query_mart("basic_arrivals")

# Arrivals overview
def layout_arrivals_overview():
    df = load_arrivals()

    st.image(ASSETS_PATH / "img" / "Arrivals_v1.png", width='stretch')

    with st.expander("Click to see information about the page"):
        st.write(""" **Arrivals Overview – Delayed arrivals at Swedish airports**
    
    This page gives you an overview of arriving flights at Swedish airports, with a focus on delays.
    Use the interactive filters to select a specific airport and adjust the date range 
    to dive deeper into the data.
    
    **What you can see:**
    
    - **Key metrics** – total number of arrivals, number of delayed arrivals, share of delayed arrivals (%), and number of on-time arrivals.
    - **Delay distribution** – a pie chart showing how delayed arrivals are distributed across different delay times.
    - **Top 5 delayed airlines** – a bar chart ranking the top 5 airlines with the most delayed arrivals.
    
    All data is filterable, so you can easily tailor the view to what you want to explore.
    """)

    # Airport selectbox
    selected_airport = pick_airport(df)

    # Date slider
    selected_dates = pick_date(df)

    # Apply filters from date and airport
    filtered_df = apply_filters(df, selected_airport, selected_dates)

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
            value=filtered_df["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"].sum()/filtered_df["AMOUNT_OF_FLIGHTS"].sum(),
            format="percent"
        )
    with cols[3]:
        st.metric(
            label="On Time Arrivals",
            value=filtered_df["AMOUNT_NOT_DELAYED_ARRIVAL"].sum()
        )

    cols2 = st.columns(2)

    with cols2[0]:
        pie_chart_late(filtered_df,"ARRIVAL_DELAYED_TIME")

    with cols2[1]:
        st.info(body="""
        **Delay distribution**

        This pie chart shows how the delayed arrivals are distributed across different delay time intervals
        (e.g. 5_to_19 min, 60_to_180 min). 

        Flights that arrived on time are excluded, so all slices
        together represent delayed flights for your current filter selection.
        """)

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
