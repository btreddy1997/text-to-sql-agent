import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_schema, execute_query, format_results
from sql_agent import generate_sql
from explainer import summarize

DB_PATH = "amazon_store.db"

questions = [
    "Who are the top 5 customers by total spend?",
    "What is the total revenue by product category?",
    "How many orders were placed each month in 2024?",
]

schema = get_schema(DB_PATH)

for question in questions:
    print("=" * 50)
    print(f"QUESTION: {question}")
    print("-" * 50)

    sql     = generate_sql(question, schema)
    results = execute_query(DB_PATH, sql)
    table   = format_results(results)
    answer  = summarize(question, sql, table)

    print(f"ANSWER: {answer}")
    print()