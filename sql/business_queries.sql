-- sql/business_queries.sql
-- These queries answer fundamental business questions about the E-Commerce store.

-- 1. Total Revenue
-- Calculates the overall total revenue generated from all orders.
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM order_items;

-- 2. Total Orders
-- Counts the total number of unique orders placed.
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- 3. Total Customers
-- Counts the total number of unique customers who made a purchase.
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM customers;

-- 4. Average Order Value (AOV)
-- Calculates the average amount spent per order.
SELECT ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM order_items;



-- 6. Monthly Revenue
-- Shows how revenue trends month over month.
SELECT 
    strftime('%Y-%m', o.order_date) AS order_month,
    ROUND(SUM(oi.revenue), 2) AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY order_month
ORDER BY order_month;

-- 7. Top 10 Customers by Revenue
-- Identifies the most valuable customers based on total spend.
SELECT 
    c.customer_id, 
    c.country, 
    ROUND(SUM(oi.revenue), 2) AS total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id
ORDER BY total_spend DESC
LIMIT 10;



-- 9. Revenue by City/Country
-- Analyzes geographical performance based on shipping country.
SELECT 
    shipping_country, 
    ROUND(SUM(oi.revenue), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY shipping_country
ORDER BY total_revenue DESC
LIMIT 10;


