import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os

st.set_page_config(page_title="Nifty Sector Tracker", layout="wide")

st.title("📈 Nifty Sector Data & Level Tracker")
st.markdown(
    "Run scripts to fetch data from TradingView and compare Current Market Price (CMP) with Support/Resistance levels.")

# Button to run python scripts
if st.button("Fetch Data and Analyze", type="primary"):
    with st.spinner("Running fetch and compare scripts..."):
        try:
            # Replace 'script1.py' and 'script2.py' with your actual filenames
            subprocess.run(["python", "script1.py"], check=True)
            subprocess.run(["python", "script2.py"], check=True)
            st.success("Scripts executed successfully!")
        except Exception as e:
            st.error(f"Error running scripts: {e}")

# Check if CSV exists and display it
csv_file = "../niftyit_fractal_levels_1day.csv"  # Replace with your actual CSV filename

if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file)

        st.subheader("Data Table")
        st.dataframe(df, use_container_width=True)

        if 'SYMBOL' in df.columns and 'SUPPORT' in df.columns and 'RESISTANCE' in df.columns:
            st.subheader("Support and Resistance Visualization")

            fig, ax = plt.subplots(figsize=(12, 6))

            x = range(len(df['SYMBOL']))
            width = 0.35

            ax.bar([i - width / 2 for i in x], df['SUPPORT'], width, label='Support', color='#ef4444')
            ax.bar([i + width / 2 for i in x], df['RESISTANCE'], width, label='Resistance', color='#22c55e')

            if 'CMP' in df.columns:
                ax.scatter(x, df['CMP'], color='#3b82f6', label='CMP', zorder=5)

            ax.set_ylabel('Price / Value')
            ax.set_title('Levels by Symbol')
            ax.set_xticks(x)
            ax.set_xticklabels(df['SYMBOL'], rotation=45, ha='right')
            ax.legend()

            st.pyplot(fig)
        else:
            st.warning("CSV must contain 'SYMBOL', 'SUPPORT', and 'RESISTANCE' columns for visualization.")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.info(f"No CSV file found at '{csv_file}'. Please run the scripts to generate data.")
