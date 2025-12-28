# MongoDB Schema Design and Analysis

## Overview
This document describes the MongoDB schema design for the FlexiMart retail platform. MongoDB is used to model customer, product, and order data in a flexible and scalable manner.

## Data Modeling Strategy
A hybrid data modeling approach is adopted:
- Customers and products are stored in separate collections.
- Orders embed order items within the same document.

This design minimizes joins and improves performance for order-related queries.

---

## Customers Collection

```json
{
  "_id": "C001",
  "first_name": "Rahul",
  "last_name": "Sharma",
  "email": "rahul.sharma@gmail.com",
  "phone": "+91-9876543210",
  "city": "Bangalore",
  "registration_date": "2023-01-15"
}
