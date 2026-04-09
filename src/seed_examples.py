import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import add_example, get_count

examples = [
    (
        "Who are the top 5 customers by total spend?",
        """SELECT c.name, ROUND(SUM(o.total_amount), 2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 5"""
    ),
    (
        "What is the revenue by product category?",
        """SELECT p.category, ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status != 'cancelled'
GROUP BY p.category
ORDER BY total_revenue DESC"""
    ),
    (
        "How many orders were placed each month in 2024?",
        """SELECT strftime('%Y-%m', o.order_date) AS month,
COUNT(*) AS order_count
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY month
ORDER BY month"""
    ),
    (
        "How many prime members do we have?",
        """SELECT COUNT(*) AS prime_member_count
FROM customers
WHERE is_prime = 1"""
    ),
    (
        "What are the best selling products by quantity?",
        """SELECT p.name, SUM(o.quantity) AS total_quantity_sold
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status != 'cancelled'
GROUP BY p.product_id, p.name
ORDER BY total_quantity_sold DESC
LIMIT 10"""
    ),
    (
        "Which customers have never placed an order?",
        """SELECT c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL"""
    ),
    (
        "What is the average order value?",
        """SELECT ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE status != 'cancelled'"""
    ),
    (
        "Show me all cancelled orders with customer names",
        """SELECT o.order_id, c.name, o.order_date,
ROUND(o.total_amount, 2) AS amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'cancelled'
ORDER BY o.order_date DESC"""
    ),
]

print("Seeding ChromaDB with proven examples...")
for question, sql in examples:
    add_example(question, sql)

print(f"\nDone. Total examples stored: {get_count()}")