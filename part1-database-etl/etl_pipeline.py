# ============================================
# FlexiMart ETL Pipeline
# Part 1 - Task 1.1
# ============================================

import pandas as pd
import mysql.connector
from dateutil import parser
import re
import os
import os


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="fleximart"
)

cursor = conn.cursor()

print("Connected to database")

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def standardize_phone(phone):
    if pd.isna(phone):
        return None
    phone = re.sub(r"\D", "", str(phone))
    if phone.startswith("0"):
        phone = phone[1:]
    if len(phone) > 10:
        phone = phone[-10:]
    return "+91-" + phone

def parse_date_safe(date_val):
    try:
        return parser.parse(str(date_val)).date()
    except:
        return None

print("Helper functions loaded")


# -----------------------------
# FILE PATH SETUP (SAFE METHOD)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

customers = pd.read_csv(os.path.join(DATA_DIR, "customers_raw.csv"))
products = pd.read_csv(os.path.join(DATA_DIR, "products_raw.csv"))
sales = pd.read_csv(os.path.join(DATA_DIR, "sales_raw.csv"))


print("CSV files loaded")

# -----------------------------
# TRANSFORM CUSTOMERS
# -----------------------------
customers.drop_duplicates(subset=["customer_id"], inplace=True)
customers.dropna(subset=["email"], inplace=True)

customers["phone"] = customers["phone"].apply(standardize_phone)
customers["registration_date"] = customers["registration_date"].apply(parse_date_safe)
customers["city"] = customers["city"].str.title()

print("Customers cleaned")

# -----------------------------
# TRANSFORM PRODUCTS
# -----------------------------
products.dropna(subset=["price"], inplace=True)
products["stock_quantity"] = products["stock_quantity"].fillna(0)
products["category"] = products["category"].str.title()
products["product_name"] = products["product_name"].str.strip()

print("Products cleaned")

# -----------------------------
# TRANSFORM SALES
# -----------------------------
sales.drop_duplicates(subset=["transaction_id"], inplace=True)
sales.dropna(subset=["customer_id", "product_id"], inplace=True)
sales["transaction_date"] = sales["transaction_date"].apply(parse_date_safe)

print("Sales cleaned")

print("ETL Step 1 (Extract + Transform) completed successfully")



# -----------------------------
# LOAD CUSTOMERS
# -----------------------------
insert_customer_sql = """
INSERT IGNORE INTO customers (first_name, last_name, email, phone, city, registration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

customer_rows = customers[[
    "first_name", "last_name", "email", "phone", "city", "registration_date"
]].values.tolist()

cursor.executemany(insert_customer_sql, customer_rows)
conn.commit()

print(f"Inserted {cursor.rowcount} customers")





# -----------------------------
# LOAD PRODUCTS
# -----------------------------
insert_product_sql = """
INSERT IGNORE INTO products (product_name, category, price, stock_quantity)
VALUES (%s, %s, %s, %s)
"""

product_rows = products[[
    "product_name", "category", "price", "stock_quantity"
]].values.tolist()

cursor.executemany(insert_product_sql, product_rows)
conn.commit()

print(f"Inserted {cursor.rowcount} products")




# -----------------------------
# LOAD ORDERS
# -----------------------------
order_map = {}

insert_order_sql = """
INSERT INTO orders (customer_id, order_date, total_amount, status)
VALUES (
    (SELECT customer_id FROM customers WHERE email = %s),
    %s,
    %s,
    %s
)
"""

for _, row in sales.iterrows():
    email = customers.loc[
        customers["customer_id"] == row["customer_id"], "email"
    ].values

    if len(email) == 0:
        continue

    total_amount = row["quantity"] * row["unit_price"]

    cursor.execute(
        insert_order_sql,
        (
            email[0],
            row["transaction_date"],
            total_amount,
            row["status"]
        )
    )
    conn.commit()
    order_map[row["transaction_id"]] = cursor.lastrowid

print("Orders inserted")





# -----------------------------
# LOAD ORDER ITEMS
# -----------------------------
insert_item_sql = """
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
VALUES (
    %s,
    (SELECT product_id FROM products WHERE product_name = %s),
    %s,
    %s,
    %s
)
"""

for _, row in sales.iterrows():
    if row["transaction_id"] not in order_map:
        continue

    subtotal = row["quantity"] * row["unit_price"]

    product_name = products.loc[
        products["product_id"] == row["product_id"], "product_name"
    ].values

    if len(product_name) == 0:
        continue

    cursor.execute(
        insert_item_sql,
        (
            order_map[row["transaction_id"]],
            product_name[0],
            row["quantity"],
            row["unit_price"],
            subtotal
        )
    )

conn.commit()
print("Order items inserted")





cursor.close()
conn.close()

print("ETL Load completed successfully")


