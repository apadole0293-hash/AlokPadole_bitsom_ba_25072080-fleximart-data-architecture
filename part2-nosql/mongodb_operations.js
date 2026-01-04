/*
====================================================
Part 2.2: MongoDB Practical Operations – FlexiMart
Note: These commands are illustrative and demonstrate
how MongoDB would be used for FlexiMart data.
====================================================
*/

/*
Operation 1: Load Data into MongoDB
Description:
Insert sample customer, product, and order documents
into their respective collections.
*/

db.customers.insertMany([
  {
    _id: "C001",
    first_name: "Rahul",
    last_name: "Sharma",
    email: "rahul@gmail.com",
    city: "Bangalore"
  }
]);

db.products.insertMany([
  {
    _id: "P001",
    product_name: "Samsung Galaxy S21",
    category: "Electronics",
    price: 45999
  },
  {
    _id: "P002",
    product_name: "Nike Running Shoes",
    category: "Fashion",
    price: 3499
  }
]);

db.orders.insertOne({
  _id: "T1001",
  customer_id: "C001",
  order_date: "2024-03-10",
  status: "Completed",
  total_amount: 49498,
  items: [
    {
      product_id: "P001",
      product_name: "Samsung Galaxy S21",
      quantity: 1,
      unit_price: 45999,
      subtotal: 45999
    }
  ]
});

/*
Operation 2: Basic Retrieval Query
Description:
Retrieve all orders placed by a specific customer.
*/

db.orders.find({ customer_id: "C001" });

/*
Operation 3: Update Operation
Description:
Update the stock quantity of a product after a sale.
*/

db.products.updateOne(
  { _id: "P001" },
  { $inc: { stock_quantity: -1 } }
);

/*
Operation 4: Aggregation Query
Description:
Calculate total sales amount grouped by product.
*/

db.orders.aggregate([
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.product_name",
      total_sales: { $sum: "$items.subtotal" }
    }
  }
]);

/*
Operation 5: Complex Aggregation Query
Description:
Generate total spending per customer across all orders.
*/

db.orders.aggregate([
  {
    $group: {
      _id: "$customer_id",
      total_spent: { $sum: "$total_amount" }
    }
  },
  { $sort: { total_spent: -1 } }
]);
