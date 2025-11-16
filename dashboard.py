import streamlit as st
import pandas as pd

# --- 1. Setup & Configuration ---
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")
st.title("📈 Stock Market Data Dashboard")

# --- 2. Load Data ---
@st.cache_data
def load_data():
    # Load the pre-calculated aggregations
    agg1 = pd.read_parquet("agg1_daily_close.parquet")
    agg2 = pd.read_parquet("agg2_sector_volume.parquet")
    agg3 = pd.read_parquet("agg3_daily_returns.parquet")
    return agg1, agg2, agg3

df_close, df_volume, df_returns = load_data()

# --- 3. Sidebar Filters ---
st.sidebar.header("Filters")

# Ticker Filter (Multiselect)
all_tickers = sorted(df_close['ticker'].unique())
selected_tickers = st.sidebar.multiselect("Select Tickers", all_tickers, default=all_tickers[:2])

# Date Filter (Slider)
# Ensure dates are datetime objects
df_close['trade_date'] = pd.to_datetime(df_close['trade_date'])
min_date = df_close['trade_date'].min().date()
max_date = df_close['trade_date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply Filters
# We filter the dataframes based on the user selection
mask_close = (df_close['trade_date'].dt.date >= start_date) & \
             (df_close['trade_date'].dt.date <= end_date) & \
             (df_close['ticker'].isin(selected_tickers))

filtered_close = df_close[mask_close]

mask_returns = (df_returns['trade_date'].dt.date >= start_date) & \
               (df_returns['trade_date'].dt.date <= end_date) & \
               (df_returns['ticker'].isin(selected_tickers))

filtered_returns = df_returns[mask_returns]

# --- 4. Visualizations ---

# Row 1: Daily Close Price
st.subheader("Daily Closing Price")
if not filtered_close.empty:
    # Pivot data for Streamlit's line_chart (Index=Date, Columns=Ticker, Values=Price)
    chart_data = filtered_close.pivot(index="trade_date", columns="ticker", values="close_price")
    st.line_chart(chart_data)
else:
    st.warning("No data available for the selected filters.")

# Row 2: Split Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Returns (%)")
    if not filtered_returns.empty:
        returns_chart = filtered_returns.pivot(index="trade_date", columns="ticker", values="daily_return")
        st.line_chart(returns_chart)
    else:
        st.warning("No data.")

with col2:
    st.subheader("Average Volume by Sector")
    # This dataset is static (no date filter applied as it's a sector overview)
    st.bar_chart(df_volume.set_index("sector"))

# --- 5. Data Preview (Optional) ---
with st.expander("View Raw Aggregated Data"):
    st.write("Daily Close Data:", filtered_close.head())