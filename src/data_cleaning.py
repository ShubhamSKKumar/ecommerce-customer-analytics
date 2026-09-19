import pandas as pd
import os

from src import config

def clean_data():
    raw_data_path = config.RAW_CSV_PATH
    cleaned_data_path = config.CLEANED_CSV_PATH

    if not os.path.exists(raw_data_path):
        print(
            f"Error: {raw_data_path} not found. Run data_ingestion.py first."
        )
        return

    print("Loading raw data...")
    df = pd.read_csv(raw_data_path, encoding="ISO-8859-1")
    print(f"Initial shape: {df.shape}")

    # 1. Drop rows with missing CustomerID
    print("Dropping rows with missing CustomerID...")
    df.dropna(subset=["CustomerID"], inplace=True)

    # 2. Remove canceled orders (InvoiceNo starts with 'C')
    print("Removing canceled orders...")
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]

    # 3. Filter out negative quantities and zero prices
    print("Filtering out invalid quantities and prices...")
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # 4. Standardize Data Types
    print("Standardizing data types...")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"] = df["CustomerID"].astype(int)

    # 5. Remove duplicates
    print("Removing duplicate rows...")
    df.drop_duplicates(inplace=True)

    # Optional: Basic Text Cleaning for Description
    df["Description"] = df["Description"].str.strip()

    print(f"Final shape: {df.shape}")

    print(f"Saving cleaned data to {cleaned_data_path}...")
    df.to_csv(cleaned_data_path, index=False)
    print("Data cleaning completed successfully!")


if __name__ == "__main__":
    clean_data()
