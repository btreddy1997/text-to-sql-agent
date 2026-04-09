import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
from flask import Flask, render_template, request, jsonify
from database import get_schema, execute_query, format_results
from sql_agent import generate_sql
from explainer import summarize

app = Flask(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)

config = load_config()
DB_PATH = config["database"]["path"]
schema  = get_schema(DB_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please ask a question."})

    sql = generate_sql(question, schema)

    if "out_of_scope" in sql.lower():
        return jsonify({"error": "I can only answer questions about customers, products and orders."})

    if not sql.strip().upper().startswith("SELECT"):
        return jsonify({"error": "Could not generate a valid query. Try rephrasing."})

    results = execute_query(DB_PATH, sql)

    if not results:
        return jsonify({"error": "No results found for that question."})

    table  = format_results(results)
    answer = summarize(question, sql, table)

    return jsonify({
        "sql":    sql,
        "table":  table,
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)