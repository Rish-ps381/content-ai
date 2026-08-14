from __future__ import annotations

from pathlib import Path
from typing import List, Dict

from .memory import memory
from .safety import validate_sql
from .tiger_gateway_client import TigerGatewayClient, TigerGatewayError
from .graph import run_retail_state_graph

SCHEMA_FILE = Path(__file__).resolve().parent.parent / "database" / "mysql_schema.sql"

STARTUP_HELP = """
Retail SQL Data Analyst Agent
Ask natural-language retail business questions and get grounded answers from the database.
Type 'exit' or 'quit' to close.

Example questions:
- What were total sales by region last month?
- Which products had the highest return rate?
- How many customers signed up in 2026 by city?
- What is the average discount percentage for online sales?
- Which stores have the most orders pending delivery?
"""


def load_schema_text() -> str:
    if not SCHEMA_FILE.exists():
        return ""

    return SCHEMA_FILE.read_text(encoding="utf-8").strip()


def print_result(question: str, sql: str, rows: List[Dict[str, object]], answer: str) -> None:
    print("\n=== Result ===")
    print(f"Question: {question}")
    print(f"Generated SQL: {sql}")
    print(f"Rows returned: {len(rows)}")
    print(f"Answer: {answer}")
    print("============\n")


def main() -> None:
    schema_text = load_schema_text()

    print(STARTUP_HELP)

    while True:
        user_input = input("Ask a question> ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        memory.add_user_message(user_input)

        try:
            graph_output = run_retail_state_graph(
                user_input,
                schema_text,
                memory.get_recent_messages(),
                client_factory=TigerGatewayClient,
            )
            sql = validate_sql(graph_output.get("sql", ""))
            rows = graph_output.get("rows", [])
            answer = graph_output.get("answer", "The query returned no results.")
        except ValueError as exc:
            print(f"Safety error: {exc}")
            continue
        except TigerGatewayError as exc:
            print(f"LLM error: {exc}")
            continue

        print_result(user_input, sql, rows, answer)
        memory.add_assistant_message(answer, generated_sql=sql)


if __name__ == "__main__":
    main()
