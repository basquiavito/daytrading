import streamlit as st
import yfinance as yf
import pandas as pd

# Set pandas display options (from your script)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)

# Streamlit app title
st.title("OHLC and Volume Viewer")

# Sidebar for user input
st.sidebar.header("Input Options")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", value="AAPL")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
timeframe = st.sidebar.selectbox(
    "Select Timeframe:",
    options=["15m", "30m", "60m", "1d"],
    index=0  # Default to "15m"
)

# Fetch stock data
if st.sidebar.button("Fetch Data"):
    try:
        # Download data using yfinance
        intraday = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval=timeframe,
            progress=False
        )

        # Ensure data is not empty
        if intraday.empty:
            st.error(f"No data fetched for ticker {ticker}. Please check the inputs.")
        else:
            # Select only OHLC and Volume columns
            ohlc_volume = intraday[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Display the data
            st.write(f"OHLC and Volume data for {ticker} ({timeframe} timeframe):")
            st.dataframe(ohlc_volume)

    except Exception as e:
        st.error(f"An error occurred: {e}")
