import os
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

def summarize(question, sql, formatted_results):
    config = load_config()
    client = get_client()

    system_prompt = """You are a helpful data analyst.
You will be given a business question, the SQL that was run, and the results.
Answer the question in 2-3 clear sentences using the actual numbers from the results.
Be specific. Be concise. No bullet points."""

    user_message = f"""Question: {question}

SQL that was run:
{sql}

Results:
{formatted_results}

Answer the question using these results."""

    response = client.messages.create(
        model=config["claude"]["model"],
        max_tokens=config["claude"]["max_tokens"],
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.content[0].text