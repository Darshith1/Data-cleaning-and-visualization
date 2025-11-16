import pandas as pd
import numpy as np
import os

# Files
RAW_FILE = "stock_market.csv"
CLEANED_FILE = "cleaned.parquet"

def clean_data():
    print("--- Starting Data Cleaning Process ---")
    
    # 1. Load Data
    if not os.path.exists(RAW_FILE):
        print(f"Error: {RAW_FILE} not found.")
        return
    
    df = pd.read_csv(RAW_FILE)
    
    # 2. Normalize Headers (Snake Case)
    # specific mapping to ensure strict snake_case as requested
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(' ', '_', regex=False)
                  .str.replace(r'[^\w]', '', regex=True) # remove special chars
                 )
    print(f"New Headers: {list(df.columns)}")

    # 3. Standardize "Empty" Values
    # We map all variations of "null" to actual NumPy NaN
    null_values = ["", "NA", "N/A", "null", "NaN", "nan", "-", "na"]
    df.replace(null_values, np.nan, inplace=True)

    # 4. Clean Text Columns (Strings)
    # Trim whitespace and ensure consistent casing for string columns
    string_cols = ['ticker', 'sector', 'currency', 'exchange', 'validated', 'notes']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
            # Convert string "NAN" back to real NaN after upper() conversion
            df[col] = df[col].replace('NAN', None)

    # 5. Fix Date Format (Target: yyyy-MM-dd)
    if 'trade_date' in df.columns:
        # Coerce errors ensures garbage dates become NaT (Not a Time)
        df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce')
        # Drop rows where date failed to parse (optional, but good practice for time-series)
        df = df.dropna(subset=['trade_date'])

    # 6. Enforce Numeric Schema
    # Force these columns to numeric, turning errors (like text in price fields) into NaN
    numeric_cols = ['open_price', 'close_price', 'volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 7. Deduplicate
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_rows - len(df)} duplicate rows.")

    # 8. Final Schema Check & Save
    print("\n--- Final Types ---")
    print(df.dtypes)
    
    print(f"\nSaving to {CLEANED_FILE}...")
    df.to_parquet(CLEANED_FILE)
    print("Success! Cleaned data saved.")

if __name__ == "__main__":
    clean_data()