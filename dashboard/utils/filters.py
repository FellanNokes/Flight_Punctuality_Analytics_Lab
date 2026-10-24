import streamlit as st
import pandas as pd
from utils.charts import pie_chart_late

def pick_airport(df: pd.DataFrame, column: str = "AIRPORT_NAME")-> str:
    """
    Renders a Streamlit selectbox for choosing an airport.

    Adds an "All airports" default option to the unique list of airports 
    found in the specified DataFrame column.

    Args:
        df (pd.DataFrame): The flight data containing airport information.
        column (str): The column name to extract unique airport names from. Defaults to "AIRPORT_NAME".

    Returns:
        str: The name of the selected airport, or "All airports".
    """    
    airport_options = ["All airports"] + df["AIRPORT_NAME"].unique().tolist()

    selected_airport = st.selectbox(label="Choose swedish airport",options=airport_options)
    return selected_airport

def pick_date(df: pd.DataFrame, column: str = "DATE") -> tuple:
    """
    Renders a Streamlit slider for selecting a date range.

    Automatically extracts the minimum and maximum dates from the specified 
    column to set the boundaries and default values of the slider.

    Args:
        df (pd.DataFrame): The flight data containing dates.
        column (str): The column name to extract dates from. Defaults to "DATE".

    Returns:
        tuple: A tuple containing the selected start date and end date.
    """
    min_date = df["DATE"].min()
    max_date = df["DATE"].max()
        
    selected_dates = st.slider(
        label="Choose date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
        )

    return selected_dates

def apply_filters(df: pd.DataFrame, selected_airport: str, selected_dates: tuple) -> pd.DataFrame:
    """
    Filters the flight DataFrame based on the selected airport and date range.

    If "All airports" is selected, the airport filter is bypassed. The data 
    is then strictly filtered to fall within the selected date range.

    Args:
        df (pd.DataFrame): The original, unfiltered flight data.
        selected_airport (str): The specific airport name to filter by, or "All airports".
        selected_dates (tuple): A tuple containing the (start_date, end_date) bounds.

    Returns:
        pd.DataFrame: A new DataFrame containing only the filtered rows.
    """

    if selected_airport == "All airports":
        filtered_df = df
    else:
        filtered_df = df[df["AIRPORT_NAME"] == selected_airport]

    filtered_df = filtered_df[
        (filtered_df["DATE"] >= selected_dates[0]) & 
        (filtered_df["DATE"] <= selected_dates[1])
    ]

    return filtered_df