import pandas as pd
import os

# Define file paths
RAW_FILE = "stock_market.csv"

def inspect_data():
    # Check if file exists before trying to load
    if not os.path.exists(RAW_FILE):
        print(f"Error: '{RAW_FILE}' not found. Please make sure it is in the same folder as this script.")
        return

    print("--- Loading Raw Data ---")
    df = pd.read_csv(RAW_FILE)
    
    # 1. Inspect Shape
    print(f"\nShape: {df.shape} (Rows, Columns)")
    
    # 2. Preview Rows
    print("\n--- First 5 Rows ---")
    print(df.head())
    
    # 3. Schema & Null Summary
    print("\n--- Schema & Null Check ---")
    print(df.info())
    
    print("\n--- Missing Values Count ---")
    print(df.isnull().sum())

if __name__ == "__main__":
    inspect_data()