# Text to SQL Agent

Ask questions in plain English, get answers from a real database.

## What it does
- You type a question in plain English
- Claude converts it to SQL automatically
- Runs the query on a real SQLite database
- Returns results + plain English summary

## Tech Stack
- Python
- SQLite (database)
- Claude API (Anthropic)
- Flask (coming soon)

## Setup

1. Clone the repo
2. Install dependencies
   pip install -r requirements.txt
3. Create .env file
   ANTHROPIC_API_KEY=your_key_here
4. Create the database
   cd src
   python create_database.py
5. Run the agent
   cd ..
   python src/main.py

## Example
Your question: Who are the top 5 customers by total spend?

SQL:
SELECT c.name, ROUND(SUM(o.total_amount), 2) as total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5

Answer:
James Carter is the top customer with $7,019.84 in total spend,
followed by Riya Sharma at $4,409.84.
