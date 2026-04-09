import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_schema, execute_query, format_results
from sql_agent import generate_sql
from explainer import summarize

def load_db_path():
    import json
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["database"]["path"]

def run_pipeline(question, schema, db_path):
    print("\nGenerating SQL...")
    sql = generate_sql(question, schema)
    print(f"\nSQL:\n{sql}")

    print("\nRunning query...")
    results = execute_query(db_path, sql)

    if not results:
        print("\nNo results found.")
        return

    table = format_results(results)
    print(f"\nResults:\n{table}")

    print("\nSummarizing...")
    answer = summarize(question, sql, table)
    print(f"\nAnswer: {answer}")

def main():
    db_path = load_db_path()
    schema  = get_schema(db_path)

    print("=" * 50)
    print("Text to SQL Agent")
    print("Type your question. Type 'exit' to quit.")
    print("=" * 50)

    while True:
        print()
        question = input("Your question: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            run_pipeline(question, schema, db_path)
        except Exception as e:
            print(f"\nSomething went wrong: {e}")
            print("Try rephrasing your question.")

if __name__ == "__main__":
    main()