import streamlit as st
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent / "outputs" / "forecasts"

st.set_page_config(page_title="Changi Rainfall Forecast", layout="wide")
st.title("Changi Rainfall Forecast: Jul 2020 to Jun 2021")
st.write("SARIMA forecasts built from NEA Changi Climate Station data (Jan 1982 to Jun 2020).")

choice = st.radio(
    "Choose forecast",
    ["Monthly total rainfall (mm)", "Highest daily rainfall in month (mm)"],
)
file = (
    "forecast_total_next_12_months.csv"
    if choice.startswith("Monthly")
    else "forecast_max_daily_next_12_months.csv"
)

f = pd.read_csv(BASE / file, index_col=0, parse_dates=True)
st.line_chart(f[["forecast", "lower", "upper"]])
st.dataframe(f.round(1))

st.info(
    "The 'lower' and 'upper' lines form a 95% prediction interval. It is wide because "
    "monthly rainfall is highly variable; the forecast mainly captures the seasonal pattern "
    "(wetter Nov to Jan), not individual extreme months."
)
st.caption("Data: National Environment Agency, Changi Climate Station, via data.gov.sg.")
