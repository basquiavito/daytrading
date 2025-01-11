import streamlit as st
import yfinance as yf
import pandas as pd

# Set pandas display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)

# Streamlit app title
st.title("OHLC, Scaled Volume, OC, and Range Viewer")

# Sidebar for user input
st.sidebar.header("Input Options")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", value="AAPL")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
timeframe = st.sidebar.selectbox(
    "Select Timeframe:",
    options=["2m", "5m", "15m", "30m", "60m", "1d"],
    index=2  # Default to "15m"
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
            # Convert the index to 12-hour format with AM/PM
            intraday.index = intraday.index.strftime('%Y-%m-%d %I:%M %p')

            # Check for missing values in essential columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in intraday.columns]

            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}. Please check the data source.")
                st.stop()

            # Drop rows with missing values in essential columns
            if intraday[required_columns].isnull().any().any():
                st.warning("Missing values detected in essential columns. Dropping rows with NaNs.")
                intraday.dropna(subset=required_columns, inplace=True)

            # Calculate additional columns: RV (scaled volume), OC (Close - Open), and Range (High - Low)
            intraday['RV'] = intraday['Volume'] / 10000
            intraday['OC'] = intraday['Close'] - intraday['Open']
            intraday['Range'] = intraday['High'] - intraday['Low']

            # Debugging: Check column names
            st.write("Debugging: Column Names")
            st.write(intraday.columns.tolist())

            # Select and display required columns including RV, OC, and Range
            ohlc_volume_oc_range = intraday[['Open', 'High', 'Low', 'Close', 'RV', 'OC', 'Range']]

            # Display the data using st.table to ensure proper column names are shown
            st.write(f"OHLC, Scaled Volume (RV), OC, and Range for {ticker} ({timeframe} timeframe):")
            st.table(ohlc_volume_oc_range)

    except Exception as e:
        st.error(f"An error occurred: {e}")
