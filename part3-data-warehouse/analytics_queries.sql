-- ============================================
-- Analytical Queries for FlexiMart
-- ============================================

-- 1. Total sales by product
SELECT 
    p.product_name,
    SUM(f.total_sales) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_revenue DESC;

-- 2. Total sales by customer city
SELECT 
    c.city,
    SUM(f.total_sales) AS city_sales
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.city
ORDER BY city_sales DESC;

-- 3. Monthly sales trend
SELECT 
    d.year,
    d.month,
    SUM(f.total_sales) AS monthly_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 4. Top 5 customers by revenue
SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(f.total_sales) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 5;
