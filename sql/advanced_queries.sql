-- sql/advanced_queries.sql
-- These queries demonstrate advanced SQL techniques (CTEs, Window Functions) to extract deeper insights.

-- 1. Repeat Customer Percentage
-- Calculates the percentage of customers who have made more than one purchase.
WITH CustomerOrderCounts AS (
    SELECT customer_id, COUNT(DISTINCT order_id) as order_count
    FROM orders
    GROUP BY customer_id
)
SELECT 
    COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers,
    COUNT(*) AS total_customers,
    ROUND(CAST(COUNT(CASE WHEN order_count > 1 THEN 1 END) AS FLOAT) / COUNT(*) * 100, 2) AS repeat_customer_percentage
FROM CustomerOrderCounts;

-- 2. Monthly Revenue Growth (MoM)
-- Uses window functions to calculate Month-over-Month revenue growth percentage.
WITH MonthlyRevenue AS (
    SELECT 
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.revenue) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY order_month
)
SELECT 
    order_month,
    ROUND(revenue, 2) AS current_revenue,
    ROUND(LAG(revenue) OVER (ORDER BY order_month), 2) AS previous_month_revenue,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY order_month)) / LAG(revenue) OVER (ORDER BY order_month)) * 100, 2) AS growth_percentage
FROM MonthlyRevenue;

-- 3. Customers with No Purchase in the Last 90 Days (At-Risk)
-- Identifies customers who haven't purchased recently.
WITH LastPurchase AS (
    SELECT 
        customer_id, 
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id, 
    last_order_date,
    CAST(julianday('2011-12-10') - julianday(last_order_date) AS INTEGER) AS days_since_last_purchase
FROM LastPurchase
WHERE days_since_last_purchase > 90
ORDER BY days_since_last_purchase DESC;

-- 4. Customer Ranking using RANK()
-- Ranks customers by their total lifetime value (revenue).
WITH CustomerLTV AS (
    SELECT 
        c.customer_id,
        c.country,
        SUM(oi.revenue) AS lifetime_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
)
SELECT 
    customer_id,
    country,
    ROUND(lifetime_value, 2) AS ltv,
    RANK() OVER (ORDER BY lifetime_value DESC) AS customer_rank
FROM CustomerLTV
LIMIT 20;

-- 5. Running Monthly Revenue
-- Calculates a cumulative running total of revenue over time.
WITH MonthlyRevenue AS (
    SELECT 
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.revenue) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY order_month
)
SELECT 
    order_month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(SUM(revenue) OVER (ORDER BY order_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total_revenue
FROM MonthlyRevenue;

-- 6. Customers whose spending increased over time
-- Compares a customer's first purchase value vs their latest purchase value.
WITH CustomerPurchases AS (
    SELECT 
        o.customer_id,
        o.order_date,
        SUM(oi.revenue) AS order_value,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC) AS first_order_rank,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS latest_order_rank
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id, o.order_id
),
FirstAndLatest AS (
    SELECT 
        customer_id,
        MAX(CASE WHEN first_order_rank = 1 THEN order_value END) AS first_spend,
        MAX(CASE WHEN latest_order_rank = 1 THEN order_value END) AS latest_spend
    FROM CustomerPurchases
    GROUP BY customer_id
)
SELECT 
    customer_id,
    ROUND(first_spend, 2) AS first_spend,
    ROUND(latest_spend, 2) AS latest_spend,
    ROUND(latest_spend - first_spend, 2) AS spending_difference
FROM FirstAndLatest
WHERE latest_spend > first_spend
AND first_spend IS NOT NULL 
AND latest_spend IS NOT NULL
ORDER BY spending_difference DESC
LIMIT 10;
