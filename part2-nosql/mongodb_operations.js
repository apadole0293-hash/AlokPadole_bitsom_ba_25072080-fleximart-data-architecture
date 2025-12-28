// Find all orders of a specific customer
db.orders.find({ customer_id: "C001" });

// Find products by category
db.products.find({ category: "Electronics" });

// Find orders after a certain date
db.orders.find({ order_date: { $gte: "2024-03-01" } });

// Aggregate total sales by product
db.orders.aggregate([
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.product_name",
      totalSales: { $sum: "$items.subtotal" }
    }
  }
]);
