import streamlit as st
import pandas as pd

base_dir = "/home/rajkumar/Documents/code_stock_alert_VRZ/stock_picking/Dev/tvdatafeed_lib/sector_wise_price_notifier/"

# Set global theme font size (add this at the top of your app)
st.set_page_config(layout="wide")

st.subheader("Nifty Bank Index")
df = pd.read_csv(base_dir+"niftybank_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50) , use_container_width=True)

st.subheader("Nifty Auto Index")
df = pd.read_csv(base_dir+"niftyauto_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty FMCG Index")
df = pd.read_csv(base_dir+"niftyfmcg_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty IT Index")
df = pd.read_csv(base_dir+"niftyit_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty Pharma Index")
df = pd.read_csv(base_dir+"niftypharma_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty Reality Index")
df = pd.read_csv(base_dir+"niftyrealty_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty Media Index")
df = pd.read_csv(base_dir+"niftymedia_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Nifty Metal Index")
df = pd.read_csv(base_dir+"niftymetal_fractal_levels_1day.csv")   # change path
st.dataframe(df.head(50), use_container_width=True)