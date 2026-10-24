import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def pie_chart_late(df: pd.DataFrame, sortby:str):
    pie_df = df[df[sortby] != "On Time"]
    counts = pie_df[sortby].value_counts()

    if counts.empty:
        pie_chart = st.warning("No delayed flights for the selected airport.")
    else:
        fig, ax = plt.subplots(facecolor="#1A1A1A")
        pie = ax.pie(counts, labels=counts.index, textprops={'color': 'white'})
        ax.pie_label(pie, counts)
        pie_chart = st.pyplot(fig)

    return pie_chart