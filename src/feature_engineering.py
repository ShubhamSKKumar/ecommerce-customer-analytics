import os
import pandas as pd

from src import config

def engineer_features():
    cleaned_data_path = config.CLEANED_CSV_PATH
    engineered_data_path = config.FEATURES_CSV_PATH

    if not os.path.exists(cleaned_data_path):
        print(f"Error: {cleaned_data_path} not found. Run data_cleaning.py")
        return

    print("Loading cleaned data...")
    df = pd.read_csv(cleaned_data_path)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    print("Engineering features...")
    # 1. Revenue
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # 2. Extract Date Features
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")
    df["InvoiceYear"] = df["InvoiceDate"].dt.year
    df["InvoiceDay"] = df["InvoiceDate"].dt.day_name()

    # 3. Create a Cohort Month (Month of first purchase) for retention analysis
    df["CohortMonth"] = (
        df.groupby("CustomerID")["InvoiceDate"]
        .transform("min")
        .dt.to_period("M")
    )

    # Save the engineered dataset
    print(f"Saving engineered data to {engineered_data_path}...")
    df.to_csv(engineered_data_path, index=False)
    print("Feature engineering completed successfully!")


if __name__ == "__main__":
    engineer_features()
