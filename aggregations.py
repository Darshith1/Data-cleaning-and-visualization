import pandas as pd
import os

CLEANED_FILE = "cleaned.parquet"

def create_aggregations():
    print("--- Starting Aggregations ---")
    
    if not os.path.exists(CLEANED_FILE):
        print("Error: cleaned.parquet not found. Run the previous step first.")
        return

    # Load the clean data (much faster with parquet)
    df = pd.read_parquet(CLEANED_FILE)
    
    # --- Aggregation 1: Daily Average Close by Ticker ---
    # Groups by Date and Ticker to handle any potential intraday duplicates
    agg1 = df.groupby(['trade_date', 'ticker'])['close_price'].mean().reset_index()
    agg1.columns = ['trade_date', 'ticker', 'close_price']
    agg1.to_parquet("agg1_daily_close.parquet")
    print(f"1. Saved agg1_daily_close.parquet ({len(agg1)} rows)")

    # --- Aggregation 2: Average Volume by Sector ---
    # Groups by Sector to compare trading activity
    agg2 = df.groupby('sector')['volume'].mean().reset_index()
    agg2.columns = ['sector', 'avg_volume']
    agg2.to_parquet("agg2_sector_volume.parquet")
    print(f"2. Saved agg2_sector_volume.parquet ({len(agg2)} rows)")
    
    # --- Aggregation 3: Simple Daily Return by Ticker ---
    # Sorts by time, groups by ticker, and calculates % change
    df_sorted = df.sort_values(by=['ticker', 'trade_date'])
    df_sorted['daily_return'] = df_sorted.groupby('ticker')['close_price'].pct_change()
    
    # Drop the first row (which will be NaN) and save
    agg3 = df_sorted[['trade_date', 'ticker', 'daily_return']].dropna()
    agg3.to_parquet("agg3_daily_returns.parquet")
    print(f"3. Saved agg3_daily_returns.parquet ({len(agg3)} rows)")

if __name__ == "__main__":
    create_aggregations()