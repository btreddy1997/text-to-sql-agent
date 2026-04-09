import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_schema, execute_query, format_results

DB_PATH = "amazon_store.db"

# Test 1 — print the schema
print("=" * 50)
print("SCHEMA")
print("=" * 50)
schema = get_schema(DB_PATH)
print(schema)

# Test 2 — run a query
print("\n" + "=" * 50)
print("QUERY RESULTS")
print("=" * 50)
sql = """
    SELECT c.name, ROUND(SUM(o.total_amount), 2) as total_spent
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status != 'cancelled'
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 5
"""
results = execute_query(DB_PATH, sql)
print(format_results(results))