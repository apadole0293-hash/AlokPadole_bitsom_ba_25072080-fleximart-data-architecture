-- ============================================
-- Fact Table for Sales Analytics
-- ============================================

CREATE TABLE fact_sales (
    sales_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_key INT,
    product_key INT,
    date_key INT,
    quantity INT,
    total_sales DECIMAL(12,2),

    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
