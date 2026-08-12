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

-- 5. Total Profit (Estimated)
-- Calculates total profit using synthetic cost_price.
SELECT ROUND(SUM((oi.unit_price - p.cost_price) * oi.quantity), 2) AS total_profit
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;

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

-- 8. Top-performing Categories
-- Shows which product categories generate the most revenue.
SELECT 
    p.category, 
    ROUND(SUM(oi.revenue), 2) AS category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

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

-- 10. Discount vs Profit Analysis
-- Examines if higher discounts correlate with lower overall profit margins.
SELECT 
    oi.discount,
    COUNT(oi.order_id) as items_sold,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    ROUND(SUM((oi.unit_price - p.cost_price) * oi.quantity), 2) AS total_profit
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.discount
ORDER BY oi.discount;
