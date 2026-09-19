import pandas as pd
import sqlite3
import os
from src import config

def create_database():
    cleaned_data_path = config.FEATURES_CSV_PATH
    db_path = config.DB_PATH

    if not os.path.exists(cleaned_data_path):
        print(
            f"Error: {cleaned_data_path} not found. Run data_cleaning.py first."
        )
        return

    print("Loading engineered data...")
    df = pd.read_csv(cleaned_data_path)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    conn.cursor()

    # 1. Customers Table
    print("Creating Customers table...")
    customers = df[["CustomerID", "Country"]].drop_duplicates(
        subset=["CustomerID"]
    ).copy()

    customers.rename(
        columns={"CustomerID": "customer_id", "Country": "country"},
        inplace=True,
    )
    customers.to_sql("customers", conn, if_exists="replace", index=False)

    # 2. Products Table
    print("Creating Products table...")
    products = df[["StockCode", "Description", "UnitPrice"]].drop_duplicates(
        subset=["StockCode"]
    )
    # Sometimes one StockCode has multiple descriptions or prices, let's keep the latest or mode.
    products = products.groupby("StockCode").first().reset_index()

    products.rename(
        columns={
            "StockCode": "product_id",
            "Description": "product_name",
            "UnitPrice": "unit_price",
        },
        inplace=True,
    )
    products.to_sql("products", conn, if_exists="replace", index=False)

    # 3. Orders Table
    print("Creating Orders table...")
    orders = df[
        ["InvoiceNo", "CustomerID", "InvoiceDate", "Country"]
    ].drop_duplicates(subset=["InvoiceNo"]).copy()

    orders.rename(
        columns={
            "InvoiceNo": "order_id",
            "CustomerID": "customer_id",
            "InvoiceDate": "order_date",
            "Country": "shipping_country",
        },
        inplace=True,
    )
    orders.to_sql("orders", conn, if_exists="replace", index=False)

    # 4. Order Items Table
    print("Creating Order Items table...")
    order_items = df[
        ["InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Revenue"]
    ].copy()

    order_items.rename(
        columns={
            "InvoiceNo": "order_id",
            "StockCode": "product_id",
            "Quantity": "quantity",
            "UnitPrice": "unit_price",
            "Revenue": "revenue",
        },
        inplace=True,
    )
    order_items.to_sql("order_items", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print(
        f"Database created successfully at {db_path} with tables: customers, products, orders, order_items."
    )


if __name__ == "__main__":
    create_database()
