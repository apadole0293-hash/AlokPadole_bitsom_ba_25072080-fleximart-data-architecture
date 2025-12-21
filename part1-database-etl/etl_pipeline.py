# ============================================
# FlexiMart ETL Pipeline
# Part 1 - Task 1.1
# ============================================

import pandas as pd
import mysql.connector
from dateutil import parser
import re

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
# EXTRACT DATA
# -----------------------------
customers = pd.read_csv("../data/customers_raw.csv")
products = pd.read_csv("../data/products_raw.csv")
sales = pd.read_csv("../data/sales_raw.csv")

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
