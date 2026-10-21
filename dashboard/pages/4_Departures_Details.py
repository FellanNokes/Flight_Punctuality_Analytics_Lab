# Departures detailed filtersimport streamlit as st
import streamlit as st
from connect_data_warehouse import query_mart
from pathlib import Path
import matplotlib.pyplot as plt

ASSETS_PATH = Path(__file__).parents[1] / "assets"

@st.cache_data
def load_departures():
    return query_mart("departures_filter_mart")

# Choose All in selectbox funktion
ALL = "All"

def filter_selectbox(label, df, column):
    options = [ALL] + sorted(df[column].dropna().unique())
    choice = st.selectbox(label, options)
    if choice == ALL:
        return df
    return df[df[column] == choice]

# Departures overview
def layout_departures_overview():
    df = load_departures()

    st.image(ASSETS_PATH / "img" / "Departures_details_v1.png", width='stretch')

    with st.expander("Click to see information about the page"):
            st.write(""" **Departures Details – Delayed departures at Swedish airports**
            
This page gives you an overview of departing flights at Swedish airports, with a focus on delays.
Use the filters to select airport, date range, airline, time period, travel zone, and arrival continent and country
to dive deeper into the data.

**What you can see:**

- **Key metrics** – total number of departures, number of delayed departures, share of delayed departures (%), and number of on-time departures.
- **Delay distribution** – a pie chart showing how delayed departures are distributed across different delay times.
- **Delays by day of week** – a bar chart showing how the number of delayed departures varies across the days of the week.

All data is filterable, so you can easily tailor the view to what you want to explore.""")


    filtered_df = filter_selectbox("Choose swedish airport", df, "SWEDISH_AIRPORT_NAME")


    min_date = filtered_df["DATE"].min()
    max_date = filtered_df["DATE"].max()
            
    selected_dates = st.slider(
        label="Choose date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
        )

    filtered_df = filtered_df[
            (filtered_df["DATE"] >= selected_dates[0]) & 
            (filtered_df["DATE"] <= selected_dates[1])
        ]

    
    metrics_area = st.container()
    with metrics_area:
        metrics_cols = st.columns(4) 


    cols = st.columns(4)

    with cols[0]:
        filtered_df = filter_selectbox("Choose airline", filtered_df, "AIRLINE_NAME")

    with cols[1]:
        filtered_df = filter_selectbox("Choose time period", filtered_df, "TIME_PERIOD")

    with cols[2]:
        filtered_df = filter_selectbox("Choose travel zone", filtered_df, "TYPE_OF_FLIGHT")

    with cols[0]:
        filtered_df = filter_selectbox("Choose arrival continent", filtered_df, "ARRIVAL_CONTINENT")

    with cols[1]:
        filtered_df = filter_selectbox("Choose arrival country", filtered_df, "ARRIVAL_COUNTRY")



    cols2 = st.columns(2)

    with cols2[0]:

        pie_df = filtered_df[filtered_df["DEPARTURE_DELAYED_TIME"] != "On Time"]

        counts = pie_df["DEPARTURE_DELAYED_TIME"].value_counts()
        departure_delayed_time_options = pie_df["DEPARTURE_DELAYED_TIME"].unique().tolist()

        if counts.empty:
            st.warning("No delayed flights for the selected airport.")
        else:
            fig, ax = plt.subplots(facecolor="#1A1A1A")
            pie = ax.pie(counts, labels=departure_delayed_time_options, textprops={'color': 'white'})
            ax.pie_label(pie, counts)
            st.pyplot(fig)

    with cols2[1]:
        st.info(body="""
**Delay distribution**

This pie chart shows how the delayed arrivals are distributed across different delay time intervals
(e.g. 5_to_19 min, 60_to_180 min). 

Flights that arrived on time are excluded, so all slices
together represent delayed flights for your current filter selection.
""")


    with metrics_area:
        with metrics_cols[0]:
            st.metric(
                label="Amount of departures",
                value=filtered_df["AMOUNT_OF_FLIGHTS"].sum()
            )

        with metrics_cols[1]:
            st.metric(
                label="Delayed departures",
                value=filtered_df["AMOUNT_DELAYED_DEPARTURES"].sum()
            )

        with metrics_cols[2]:
            st.metric(
                label="Delayed departures (%)",
                value=filtered_df["AMOUNT_DELAYED_DEPARTURES"].sum()/filtered_df["AMOUNT_OF_FLIGHTS"].sum(),
                format="percent"
            )

        with metrics_cols[3]:
            st.metric(
                label="On Time Departures",
                value=filtered_df["AMOUNT_NOT_DELAYED_DEPARTURE"].sum()
            )



    sort_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    days_df = (
        filtered_df.groupby("DAY_OF_WEEK")["AMOUNT_DELAYED_DEPARTURES"]
        .sum()
        .reindex(sort_days)
        )
    
    st.bar_chart(
        days_df,
        sort=False       
        )

if __name__ == "__main__":
    layout_departures_overview()
