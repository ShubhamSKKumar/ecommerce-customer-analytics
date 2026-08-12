import pandas as pd
import sqlite3
import os


def create_database():
    cleaned_data_path = os.path.join(
        "data", "cleaned", "online_retail_features.csv"
    )
    db_path = os.path.join("ecommerce.db")

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
    )
    # Since we don't have age/gender, we'll just have ID and Country.
    # To meet project requirements, we can generate synthetic demographic data for these existing customers.
    import numpy as np

    np.random.seed(42)
    customers["gender"] = np.random.choice(
        ["Male", "Female"], size=len(customers)
    )
    customers["age"] = np.random.randint(18, 70, size=len(customers))
    customers["signup_date"] = (
        df.groupby("CustomerID")["InvoiceDate"].min().values
    )

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
    # Add synthetic product categories for depth
    categories = [
        "Electronics",
        "Apparel",
        "Home & Garden",
        "Toys",
        "Health & Beauty",
    ]
    products["category"] = np.random.choice(categories, size=len(products))
    # Synthetic cost price to allow profit calculations (e.g., 40-70% margin)
    products["cost_price"] = products["UnitPrice"] * np.random.uniform(
        0.3, 0.6, size=len(products)
    )

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
    ].drop_duplicates(subset=["InvoiceNo"])
    # Add synthetic payment method
    payment_methods = ["Credit Card", "PayPal", "Debit Card"]
    orders["payment_method"] = np.random.choice(
        payment_methods, size=len(orders)
    )

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
    # Adding synthetic discount (0-20%)
    order_items["discount"] = np.random.choice(
        [0, 0.05, 0.1, 0.15, 0.2],
        size=len(order_items),
        p=[0.6, 0.1, 0.1, 0.1, 0.1],
    )

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
