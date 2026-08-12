# Power BI Dashboard Instructions

This document explains how to import the data into Power BI, set up the Star Schema data model, and create the necessary DAX measures to build the 3-page interactive dashboard.

## 1. Data Import

1. Open Power BI Desktop.
2. Click **Get Data** -> **ODBC** (if connecting directly to `ecommerce.db` using an SQLite ODBC driver) OR simply import the CSV files directly from `data/cleaned/` if you prefer not to use an ODBC driver.
   * If importing CSVs, you will need to export the tables from the SQLite database to CSV first (or use the raw CSVs). 
   * Alternatively, you can use Python script inside Power BI: `import pandas as pd; import sqlite3; conn = sqlite3.connect('path/to/ecommerce.db'); df = pd.read_sql('SELECT * FROM orders', conn)`
3. Load all four tables: `customers`, `products`, `orders`, and `order_items`.

## 2. Data Modeling (Star Schema)

Go to the **Model View** in Power BI and create the following relationships:

* `orders[customer_id]` -> `customers[customer_id]` (Many-to-One)
* `order_items[order_id]` -> `orders[order_id]` (Many-to-One)
* `order_items[product_id]` -> `products[product_id]` (Many-to-One)

Create a dedicated **Date Table**:
Go to Modeling -> New Table and enter:
```dax
DimDate = CALENDAR(MIN(orders[order_date]), MAX(orders[order_date]))
```
Connect `DimDate[Date]` -> `orders[order_date]` (One-to-Many).

## 3. DAX Measures

Create a new table called `_Measures` to store all your metrics.

**Total Revenue:**
```dax
Total Revenue = SUM(order_items[revenue])
```

**Total Orders:**
```dax
Total Orders = DISTINCTCOUNT(orders[order_id])
```

**Total Customers:**
```dax
Total Customers = DISTINCTCOUNT(customers[customer_id])
```

**Average Order Value (AOV):**
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

**Total Profit:**
```dax
Total Profit = SUMX(order_items, (order_items[unit_price] - RELATED(products[cost_price])) * order_items[quantity])
```

**Profit Margin:**
```dax
Profit Margin = DIVIDE([Total Profit], [Total Revenue], 0)
```

**Repeat Customer Rate:**
```dax
Repeat Customer Rate = 
VAR CustomersWithMultipleOrders = 
    FILTER(
        VALUES(customers[customer_id]),
        CALCULATE(DISTINCTCOUNT(orders[order_id])) > 1
    )
RETURN DIVIDE(COUNTROWS(CustomersWithMultipleOrders), [Total Customers], 0)
```

## 4. Dashboard Layout

### Page 1: Executive Overview
* **KPI Cards (Top):** Total Revenue, Total Profit, Total Orders, Average Order Value, Profit Margin.
* **Line Chart:** `DimDate[Month-Year]` on X-axis, `[Total Revenue]` and `[Total Profit]` on Y-axis.
* **Bar Chart:** `products[category]` on Y-axis, `[Total Revenue]` on X-axis.
* **Map:** `orders[shipping_country]` as Location, `[Total Revenue]` as Bubble Size.

### Page 2: Customer Intelligence
* **Donut Chart:** (Requires importing `customer_segments` table) `Segment` on Legend, `[Total Customers]` on Values.
* **Scatter Plot:** X-axis = Frequency, Y-axis = Monetary, Details = `CustomerID`.
* **Bar Chart:** Cohort retention by month (if using cohort table).
* **Card:** Repeat Customer Rate.

### Page 3: Product & Business Insights
* **Matrix Visual:** Rows = `products[category]`, Columns = `products[product_name]`, Values = `[Total Revenue]`, `[Total Profit]`, `[Profit Margin]`.
* **Scatter Plot:** X-axis = `order_items[discount]`, Y-axis = `[Profit Margin]`.
* **Slicers (Left panel):** Date Range, Category, Country.
