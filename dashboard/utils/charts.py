import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

def pie_chart_late(df: pd.DataFrame, sortby:str)-> DeltaGenerator:
    """
    Filters flight data and renders a pie chart of delay intervals in Streamlit.

    This function excludes rows where the status is "On Time" and generates a 
    pie chart for the remaining delay categories, tailored for dark mode. 
    It displays the exact count of flights per category rather than percentages.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing flight data.
        sortby (str): The name of the column to filter and group by.

    Returns:
        DeltaGenerator: The rendered Streamlit element.
    """
    pie_df = df[df[sortby] != "On Time"]
    counts = pie_df[sortby].value_counts()

    if counts.empty:
        pie_chart = st.warning("No delayed flights for the selected airport.")
    else:
        fig, ax = plt.subplots(facecolor="#1A1A1A")
        ax.pie(
            counts,
            labels=counts.index,
            textprops={'color': 'white'},
            autopct=lambda p: f'{int(round(p * sum(counts) / 100.0))}'
        )
        
        pie_chart = st.pyplot(fig)

    return pie_chart