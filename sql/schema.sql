-- schema.sql
-- This file documents the database schema for the E-Commerce Customer Analytics project.
-- The actual database is instantiated using sqlite3 in python, but this schema represents the structure.

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    country VARCHAR(100),
    gender VARCHAR(10),
    age INTEGER,
    signup_date DATETIME
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    unit_price DECIMAL(10, 2),
    category VARCHAR(50),
    cost_price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id INTEGER,
    order_date DATETIME,
    shipping_country VARCHAR(100),
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    revenue DECIMAL(10, 2),
    discount DECIMAL(4, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
