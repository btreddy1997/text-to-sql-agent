import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite - this creates the file if it doesn't exist
conn = sqlite3.connect("amazon_store.db")
cursor = conn.cursor()

print("Creating tables...")

# ── TABLE 1: customers ──────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL,
    city          TEXT NOT NULL,
    state         TEXT NOT NULL,
    signup_date   TEXT NOT NULL,
    is_prime      INTEGER NOT NULL  -- 1 = Prime, 0 = regular
)
""")

# ── TABLE 2: products ───────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id    INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    category      TEXT NOT NULL,
    price         REAL NOT NULL,
    stock_qty     INTEGER NOT NULL
)
""")

# ── TABLE 3: orders ─────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL,
    order_date    TEXT NOT NULL,
    status        TEXT NOT NULL,  -- delivered, shipped, cancelled
    total_amount  REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
)
""")

print("Tables created.")

# ── SAMPLE DATA: customers ──────────────────────────────────────
customers = [
    (1,  "Riya Sharma",     "riya@email.com",    "Seattle",      "WA", "2022-03-15", 1),
    (2,  "James Carter",    "james@email.com",   "Austin",       "TX", "2021-07-22", 1),
    (3,  "Priya Patel",     "priya@email.com",   "New York",     "NY", "2023-01-10", 0),
    (4,  "Mike Johnson",    "mike@email.com",    "Chicago",      "IL", "2022-11-05", 1),
    (5,  "Sara Lee",        "sara@email.com",    "San Francisco","CA", "2023-06-18", 0),
    (6,  "David Kim",       "david@email.com",   "Boston",       "MA", "2021-12-01", 1),
    (7,  "Emily Davis",     "emily@email.com",   "Denver",       "CO", "2022-08-30", 0),
    (8,  "Carlos Ruiz",     "carlos@email.com",  "Miami",        "FL", "2023-02-14", 1),
    (9,  "Anita Nair",      "anita@email.com",   "Seattle",      "WA", "2022-05-20", 1),
    (10, "Tom Wilson",      "tom@email.com",     "Portland",     "OR", "2023-09-07", 0),
]

# ── SAMPLE DATA: products ───────────────────────────────────────
products = [
    (1,  "Laptop Pro 15",        "Electronics",  1299.99, 45),
    (2,  "Wireless Headphones",  "Electronics",   199.99, 120),
    (3,  "USB-C Hub",            "Electronics",    49.99, 300),
    (4,  "Python Crash Course",  "Books",          29.99, 200),
    (5,  "Clean Code",           "Books",          34.99, 150),
    (6,  "Office Chair",         "Furniture",     349.99,  30),
    (7,  "Standing Desk",        "Furniture",     599.99,  20),
    (8,  "Water Bottle",         "Kitchen",        24.99, 500),
    (9,  "Coffee Maker",         "Kitchen",        89.99,  80),
    (10, "Yoga Mat",             "Sports",         39.99, 250),
    (11, "Running Shoes",        "Sports",        119.99,  90),
    (12, "Mechanical Keyboard",  "Electronics",   149.99,  60),
]

# ── SAMPLE DATA: orders (60 rows, realistic spread) ─────────────
random.seed(42)  # same seed = same data every run

statuses = ["delivered", "delivered", "delivered", "shipped", "cancelled"]
# delivered appears 3x so it's the most common — realistic

orders = []
start_date = datetime(2024, 1, 1)

for order_id in range(1, 61):
    customer_id  = random.randint(1, 10)
    product_id   = random.randint(1, 12)
    quantity     = random.randint(1, 3)
    days_offset  = random.randint(0, 364)
    order_date   = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    status       = random.choice(statuses)

    # Look up the product price to calculate total
    price = products[product_id - 1][3]
    total = round(price * quantity, 2)

    orders.append((order_id, customer_id, product_id, quantity, order_date, status, total))

# ── INSERT DATA ─────────────────────────────────────────────────
cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?,?,?,?,?,?,?)", customers)
cursor.executemany("INSERT OR IGNORE INTO products  VALUES (?,?,?,?,?)",    products)
cursor.executemany("INSERT OR IGNORE INTO orders    VALUES (?,?,?,?,?,?,?)", orders)

conn.commit()
conn.close()

print(f"Done! Created:")
print(f"  → {len(customers)} customers")
print(f"  → {len(products)} products")
print(f"  → {len(orders)} orders")
print(f"\nDatabase saved as: amazon_store.db")
print("Open it in DB Browser for SQLite to explore!")