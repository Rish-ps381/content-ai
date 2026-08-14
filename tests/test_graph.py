from __future__ import annotations

from src.graph import (
    build_sql_generation_messages,
    create_retail_state_graph,
    extract_sql,
    format_history_for_prompt,
)


class DummyClient:
    def send_chat(self, messages):
        prompt = "\n".join(
            message["content"] for message in messages if message["role"] == "user"
        )
        if "Return only one safe MySQL SELECT statement" in prompt:
            return "SELECT * FROM stores"
        return "Based on the returned rows, stores in the south region have the highest sales."


def test_extract_sql_from_markdown_fence():
    sql = extract_sql("```sql\nSELECT * FROM stores;\n```")
    assert sql == "SELECT * FROM stores"


def test_build_sql_generation_messages_includes_schema_and_question():
    schema_text = "CREATE TABLE stores (store_id INT PRIMARY KEY, city VARCHAR(100));"
    history = [{"role": "user", "content": "What is the top store?"}]
    messages = build_sql_generation_messages("Which store has the highest sales?", schema_text, history)

    assert messages[0]["role"] == "system"
    assert "SELECT" in messages[0]["content"]
    assert schema_text in messages[1]["content"]
    assert "Which store has the highest sales?" in messages[1]["content"]


def test_format_history_for_prompt_returns_numbered_history():
    history = [
        {"role": "user", "content": "What were total sales last quarter?"},
        {"role": "assistant", "content": "I found the total sales."},
    ]
    formatted = format_history_for_prompt(history)

    assert "1. User: What were total sales last quarter?" in formatted
    assert "2. Assistant: I found the total sales." in formatted


def test_retail_state_graph_runs_with_dummy_client():
    compiled_graph = create_retail_state_graph(
        client_factory=DummyClient,
        query_runner=lambda sql: [{"store_id": 1, "city": "Delhi"}],
    )
    result = compiled_graph.invoke(
        {
            "question": "How many stores are in the database?",
            "schema_text": "CREATE TABLE stores (store_id INT PRIMARY KEY, city VARCHAR(100));",
            "recent_history": [],
        }
    )

    assert result["sql"] == "SELECT * FROM stores"
    assert result["rows"] == [{"store_id": 1, "city": "Delhi"}]
    assert result["answer"].startswith("Based on the returned rows")


def test_retail_state_graph_uses_recent_history_in_sql_generation():
    class MemoryAwareClient:
        def send_chat(self, messages):
            user_prompt = next(
                msg["content"] for msg in messages if msg["role"] == "user"
            )
            system_prompt = next(
                (msg["content"] for msg in messages if msg["role"] == "system"), ""
            )

            if "Generate exactly one valid MySQL SELECT query" in system_prompt:
                assert "1. User: What is the top store?" in user_prompt
                assert "2. Assistant: I found the top store." in user_prompt
                return "SELECT * FROM stores"

            if "Give a concise business result" in system_prompt:
                return "Based on the returned rows, stores in the south region have the highest sales."

            raise AssertionError("Unexpected prompt type in MemoryAwareClient.send_chat")

    compiled_graph = create_retail_state_graph(
        client_factory=MemoryAwareClient,
        query_runner=lambda sql: [{"store_id": 1, "city": "Delhi"}],
    )
    result = compiled_graph.invoke(
        {
            "question": "Follow-up question",
            "schema_text": "CREATE TABLE stores (store_id INT PRIMARY KEY, city VARCHAR(100));",
            "recent_history": [
                {"role": "user", "content": "What is the top store?"},
                {"role": "assistant", "content": "I found the top store."},
            ],
        }
    )

    assert result["sql"] == "SELECT * FROM stores"
    assert result["rows"] == [{"store_id": 1, "city": "Delhi"}]
    assert result["answer"].startswith("Based on the returned rows")
