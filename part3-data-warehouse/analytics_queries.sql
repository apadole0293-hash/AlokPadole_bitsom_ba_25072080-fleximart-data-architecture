-- ============================================================
-- Part 3.2: Analytical Queries on FlexiMart Data Warehouse
-- Star Schema: fact_sales, dim_customer, dim_product, dim_date
-- ============================================================


/*
Query 1: Total Revenue by Product Category
Business Question:
Which product categories generate the highest total revenue?
*/

SELECT
    p.category,
    SUM(f.total_sales) AS total_revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------

/*
Query 2: Top 5 Products by Revenue
Business Question:
Which products contribute the most to overall sales revenue?
*/

SELECT
    p.product_name,
    SUM(f.total_sales) AS product_revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY product_revenue DESC
LIMIT 5;


-- ------------------------------------------------------------

/*
Query 3: Monthly Sales Trend
Business Question:
How does total sales revenue change month over month?
*/

SELECT
    d.year,
    d.month,
    SUM(f.total_sales) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ------------------------------------------------------------

/*
Query 4: Cumulative Revenue Over Time (Window Function)
Business Question:
What is the cumulative sales revenue over time?
*/

SELECT
    d.year,
    d.month,
    SUM(f.total_sales) AS monthly_revenue,
    SUM(SUM(f.total_sales)) OVER (
        ORDER BY d.year, d.month
    ) AS cumulative_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ------------------------------------------------------------

/*
Query 5: Top Customers by Lifetime Value
Business Question:
Who are the top customers based on total spending?
*/

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.city,
    SUM(f.total_sales) AS lifetime_value
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_key, c.first_name, c.last_name, c.city
ORDER BY lifetime_value DESC
LIMIT 5;


-- ------------------------------------------------------------

/*
Query 6: Sales Contribution Percentage by Category
Business Question:
What percentage of total sales does each category contribute?
*/

SELECT
    p.category,
    SUM(f.total_sales) AS category_sales,
    ROUND(
        SUM(f.total_sales) * 100.0 /
        SUM(SUM(f.total_sales)) OVER (),
        2
    ) AS sales_percentage
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY sales_percentage DESC;
