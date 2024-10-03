# This web app is feeded with real time Bitcoin data from my local Postgresql DB and displays real time plots a Histogram and a Line plot of close prices over time. Both are being updated in real time.
# The goal is to represent visually  in real time how the close price data is distributed over time for further analysis. 


import time 
import psycopg2  
import pandas as pd 
import plotly.express as px  
import streamlit as st  
import logging  
import warnings  
from password import word

# Set Streamlit page configuration
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    filename='app_d+p.log',  # log file name
    level=logging.INFO,  # logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # log message format
)

# Function to fetch 'Close' data from PostgreSQL without caching
def fetch_data() -> pd.DataFrame:
    conn = psycopg2.connect(
        dbname="BinanceLiveDB",
        user="postgres",
        password=word,
    )
    query = "SELECT \"Timestamp\", \"Close\" FROM ohlc_data ORDER BY \"Timestamp\" ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Dashboard title
st.title("Real-Time Histogram & Price Chart of BTC  🐿🎈  " )

# Creating a single-element container for real-time histogram, line chart, and logging
placeholder = st.empty()
log_placeholder = st.empty()

# Track the previous 'Close' values to detect new arrivals
previous_data = pd.DataFrame()

# Real-time / live data update loop
for seconds in range(200):

    # Re-fetch the data every second to simulate real-time update
    df = fetch_data()

    # Compare with previous data to detect new entries
    if not df.equals(previous_data):
        # Get the latest 'Close' and 'Timestamp'
        latest_close = df['Close'].iloc[-1]
        latest_timestamp = df['Timestamp'].iloc[-1]

        # Log the latest Close and Timestamp to the log file
        logging.info(f"New Close Price {latest_close} added to the histogram at {latest_timestamp}")

        # Log the latest Close and Timestamp to the Streamlit app
        with log_placeholder.container():
            st.write(f"At {latest_timestamp}, Close Price: {latest_close}")

        with placeholder.container():
            # Create two columns for the histogram and line chart
            col1, col2 = st.columns(2)

            # Display the histogram of Close Prices in the first column
            with col1:
                st.markdown("### Close Price Histogram")
                fig_hist = px.histogram(data_frame=df, x="Close", nbins=1000, height=850, width=950)
                st.write(fig_hist)

            # Display the line chart of Close Prices (twisted) in the second column
            with col2:
                st.markdown("### Twisted Close Price Line Chart (Price on X, Time on Y)")
                fig_line = px.line(data_frame=df, x="Close", y="Timestamp", height=850, width=950)
                st.write(fig_line)

        # Update the previous data reference
        previous_data = df.copy()

    else:
        # If no new data, log and display a message
        logging.info("No new data received.")
        with log_placeholder.container():
            st.write("No new data received at this moment.")

    # Simulate real-time delay
    time.sleep(1)
