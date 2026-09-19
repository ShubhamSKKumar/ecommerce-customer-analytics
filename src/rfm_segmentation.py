import pandas as pd
import os
import datetime as dt

from src import config

def calculate_rfm():
    engineered_data_path = config.FEATURES_CSV_PATH
    rfm_path = config.SEGMENTS_CSV_PATH

    if not os.path.exists(engineered_data_path):
        print(f"Error: {engineered_data_path} not found.")
        return

    print("Loading engineered data for RFM Analysis...")
    df = pd.read_csv(engineered_data_path)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Calculate RFM Metrics
    # Reference date is +1 day from the max date in the dataset
    ref_date = df["InvoiceDate"].max() + dt.timedelta(days=1)

    print("Calculating R, F, M values...")
    rfm = (
        df.groupby("CustomerID")
        .agg(
            {
                "InvoiceDate": lambda x: (ref_date - x.max()).days,
                "InvoiceNo": "nunique",
                "Revenue": "sum",
            }
        )
        .reset_index()
    )

    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]

    # Remove negative monetary values just in case
    rfm = rfm[rfm["Monetary"] > 0]

    print("Assigning RFM scores...")
    # 5 is best for Frequency and Monetary, 5 is best (lowest) for Recency
    rfm["R_score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(
        int
    )
    # Use rank(method='first') for frequency to avoid duplicate edges error due to many 1s
    rfm["F_score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)
    rfm["M_score"] = pd.qcut(
        rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Combine scores
    rfm["rfm_score"] = (
        rfm["R_score"].astype(str)
        + rfm["F_score"].astype(str)
        + rfm["M_score"].astype(str)
    )

    print("Assigning customer segments...")

    # Define segmentation rules
    def assign_segment(row):
        r, f, m = row["R_score"], row["F_score"], row["M_score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 3 and m >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New Customers"
        elif r >= 3 and f <= 3:
            return "Potential Loyalists"
        elif r == 2 and f >= 3 and m >= 3:
            return "At Risk"
        elif r <= 1 and f >= 4 and m >= 4:
            return "Cannot Lose Them"
        elif r <= 2 and f <= 2:
            return "Hibernating"
        elif r <= 1 and f <= 1:
            return "Lost Customers"
        else:
            return "Average Customers"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    print(f"Segment Distribution:\n{rfm['Segment'].value_counts()}")

    print(f"Saving RFM segments to {rfm_path}...")
    rfm.to_csv(rfm_path, index=False)

    # Also save it to the sqlite db
    import sqlite3

    db_path = config.DB_PATH
    print("Saving segments to SQLite database...")
    conn = sqlite3.connect(db_path)
    rfm.rename(columns={"CustomerID": "customer_id"}, inplace=True)
    rfm.to_sql("customer_segments", conn, if_exists="replace", index=False)
    conn.close()
    print("RFM segmentation completed successfully!")


if __name__ == "__main__":
    calculate_rfm()
