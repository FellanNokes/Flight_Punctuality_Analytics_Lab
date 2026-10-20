import streamlit as st
from connect_data_warehouse import query_mart
from pathlib import Path
import matplotlib.pyplot as plt

ASSETS_PATH = Path(__file__).parents[1] / "assets"

@st.cache_data
def load_arrivals():
    return query_mart("arrivals_filter_mart")

# Choose All in selectbox funktion
ALL = "All"

def filter_selectbox(label, df, column):
    options = [ALL] + sorted(df[column].dropna().unique())
    choice = st.selectbox(label, options)
    if choice == ALL:
        return df
    return df[df[column] == choice]

# Arrivals overview
def layout_arrivals_overview():
    df = load_arrivals()

    st.image(ASSETS_PATH / "img" / "Arrivals_v1.png", width='stretch') # TODO: change to arrivals details image

    st.info(body="The Arrivals Overview provides a comprehensive snapshot of flight arrivals, highlighting key metrics and trends.")


    filtered_df = filter_selectbox("Choose swedish airport", df, "AIRPORT_NAME")

    
    cols = st.columns(4)

    with cols[0]:
        st.metric(
            label="Amount of arrivals",
            value=filtered_df["AMOUNT_OF_FLIGHTS"].sum()
        )

        filtered_df = filter_selectbox("Choose airline", filtered_df, "AIRLINE_NAME")

        filtered_df = filter_selectbox("Choose continent", filtered_df, "CONTINENT")
        
    with cols[1]:
        st.metric(
            label="Delayed arrivals",
            value=filtered_df["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"].sum()
        )

        filtered_df = filter_selectbox("Choose time period", filtered_df, "TIME_PERIOD")
        

        filtered_df = filter_selectbox("Choose country", filtered_df, "COUNTRY")

    with cols[2]:
        st.metric(
            label="Delayed arrivals (%)",
            value=filtered_df["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"].sum()/filtered_df["AMOUNT_OF_FLIGHTS"].sum()
        )

        filtered_df = filter_selectbox("Choose travel zone", filtered_df, "TYPE_OF_FLIGHT")

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




    sort_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    days_df = (
        filtered_df.groupby("DAY_OF_WEEK")["AMOUNT_DELAYED_FLIGHTS_ARRIVALS"]
        .sum()
        .reindex(sort_days)
        )
    
    st.bar_chart(
        days_df,
        sort=False       
        )

if __name__ == "__main__":
    layout_arrivals_overview()
