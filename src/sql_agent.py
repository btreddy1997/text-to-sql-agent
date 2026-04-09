import os
import re
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    return anthropic.Anthropic(api_key=api_key)

def extract_sql(text):
    # Remove ```sql ... ``` or ``` ... ``` if Claude adds them
    text = re.sub(r"```sql\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()

def generate_sql(question, schema):
    config = load_config()
    client = get_client()

    system_prompt = f"""You are an expert SQL assistant working with a SQLite database.

Here is the exact database schema:

{schema}

Rules you must follow:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no ```sql fences
- Use only the table names and column names shown in the schema above
- For revenue calculations always exclude cancelled orders (status != 'cancelled')
- Use ROUND(value, 2) for all decimal numbers
- Always use table aliases (o for orders, c for customers, p for products)
"""

    response = client.messages.create(
        model=config["claude"]["model"],
        max_tokens=config["claude"]["max_tokens"],
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    raw_sql = response.content[0].text
    clean_sql = extract_sql(raw_sql)
    return clean_sql