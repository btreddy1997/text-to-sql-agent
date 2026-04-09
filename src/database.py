import sqlite3
import json
import os

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # rows behave like dicts, not just tuples
    return conn

def get_schema(db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema_parts = []

    for table in tables:
        table_name = table["name"]

        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Get foreign key info
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()

        # Build FK lookup: column_name → referenced table
        fk_map = {}
        for fk in foreign_keys:
            fk_map[fk["from"]] = fk["table"]

        # Format each column
        col_descriptions = []
        for col in columns:
            col_name = col["name"]
            col_type = col["type"]
            if not col_type:        # ← skip constraint lines, they have no type
                continue
            is_pk    = " PRIMARY KEY" if col["pk"] else ""
            fk_ref   = f" FK→{fk_map[col_name]}" if col_name in fk_map else ""
            col_descriptions.append(f"  {col_name} ({col_type}{is_pk}{fk_ref})")

        schema_parts.append(f"TABLE {table_name}:\n" + "\n".join(col_descriptions))

    conn.close()
    return "\n\n".join(schema_parts)

def execute_query(db_path, sql):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    # Convert Row objects to plain dicts
    results = [dict(row) for row in rows]

    conn.close()
    return results

def format_results(results):
    if not results:
        return "No results found."

    # Column headers from first row keys
    headers = list(results[0].keys())

    # Find max width for each column
    col_widths = {h: len(h) for h in headers}
    for row in results:
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(row[h])))

    # Build the table string
    header_row    = " | ".join(h.ljust(col_widths[h]) for h in headers)
    separator     = "-+-".join("-" * col_widths[h] for h in headers)
    data_rows     = [
        " | ".join(str(row[h]).ljust(col_widths[h]) for h in headers)
        for row in results
    ]

    return "\n".join([header_row, separator] + data_rows)