from __future__ import annotations

import pytest

from src.config import ConfigError, get_settings
from src.graph import create_retail_state_graph
from src.memory import ConversationMemory
from src.safety import validate_sql


def test_select_sql_is_allowed() -> None:
    sql = "SELECT store_id, city FROM stores"
    assert validate_sql(sql) == sql


@pytest.mark.parametrize("sql", [
    "DELETE FROM stores WHERE store_id = 1",
    "DELETE FROM stores;",
    "DELETE /* comment */ FROM stores",
])
def test_delete_sql_is_blocked(sql: str) -> None:
    with pytest.raises(ValueError, match="Only SELECT statements are allowed"):
        validate_sql(sql)


@pytest.mark.parametrize("sql", [
    "UPDATE stores SET city = 'New Delhi' WHERE store_id = 1",
    "UPDATE stores SET city = 'New Delhi' WHERE store_id = 1;",
])
def test_update_sql_is_blocked(sql: str) -> None:
    with pytest.raises(ValueError, match="Only SELECT statements are allowed"):
        validate_sql(sql)


@pytest.mark.parametrize("sql", [
    "DROP TABLE stores",
    "DROP TABLE stores;",
])
def test_drop_sql_is_blocked(sql: str) -> None:
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql(sql)


@pytest.mark.parametrize("sql", [
    "TRUNCATE TABLE stores",
    "TRUNCATE TABLE stores;",
])
def test_truncate_sql_is_blocked(sql: str) -> None:
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql(sql)


def test_multiple_statements_are_blocked() -> None:
    with pytest.raises(ValueError, match="Multiple SQL statements are not allowed"):
        validate_sql("SELECT * FROM stores; SELECT * FROM products")


def test_empty_sql_is_blocked() -> None:
    with pytest.raises(ValueError, match="SQL statement is empty"):
        validate_sql("")


def test_trailing_semicolon_is_stripped() -> None:
    sql = validate_sql("SELECT city FROM stores;")
    assert sql == "SELECT city FROM stores"


def test_memory_stores_recent_conversation_context() -> None:
    memory = ConversationMemory(max_exchanges=3)
    memory.add_exchange(
        user_message="What is the highest-selling product?",
        assistant_message="I found the top product.",
        generated_sql="SELECT product_id, SUM(units_sold) FROM sales_transactions GROUP BY product_id;",
    )

    recent = memory.get_recent_exchanges()
    assert len(recent) == 1
    assert recent[0].user_message == "What is the highest-selling product?"
    assert "SELECT product_id" in recent[0].generated_sql


def test_memory_retrieves_previous_context() -> None:
    memory = ConversationMemory(max_exchanges=2)
    memory.add_user_message("First question")
    memory.add_assistant_message("First answer", generated_sql="SELECT 1")
    memory.add_exchange("Second question", "Second answer", generated_sql="SELECT 2")

    messages = memory.get_recent_messages()
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "First question"
    assert messages[1]["role"] == "assistant"
    assert "Generated SQL" in messages[1]["content"]
    assert messages[2]["content"] == "Second question"


def test_empty_sql_results_are_handled() -> None:
    class DummyClient:
        def send_chat(self, messages):
            return "SELECT 1 FROM stores"

    compiled_graph = create_retail_state_graph(
        client_factory=DummyClient,
        query_runner=lambda sql: [],
    )
    result = compiled_graph.invoke(
        {
            "question": "Do any stores exist?",
            "schema_text": "CREATE TABLE stores (store_id INT);",
            "recent_history": [],
        }
    )

    assert result["rows"] == []
    assert result["answer"] == "The query returned no results."


def test_sql_result_rows_are_dictionaries() -> None:
    class DummyClient:
        def send_chat(self, messages):
            return "SELECT store_id, city FROM stores"

    compiled_graph = create_retail_state_graph(
        client_factory=DummyClient,
        query_runner=lambda sql: [{"store_id": 5, "city": "Mumbai"}],
    )
    result = compiled_graph.invoke(
        {
            "question": "List one store.",
            "schema_text": "CREATE TABLE stores (store_id INT, city VARCHAR(100));",
            "recent_history": [],
        }
    )

    assert isinstance(result["rows"], list)
    assert result["rows"] == [{"store_id": 5, "city": "Mumbai"}]


def test_configuration_validation(monkeypatch) -> None:
    import src.config as config

    monkeypatch.delenv("MYSQL_DATABASE", raising=False)
    monkeypatch.delenv("MYSQL_USER", raising=False)
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)
    monkeypatch.delenv("TIGER_AI_GATEWAY_URL", raising=False)
    monkeypatch.delenv("TIGER_AI_GATEWAY_API_KEY", raising=False)
    monkeypatch.delenv("TIGER_AI_GATEWAY_MODEL", raising=False)
    config._settings = None

    with pytest.raises(ConfigError, match="Missing required environment variable"):
        get_settings()

    monkeypatch.setenv("MYSQL_DATABASE", "agentic_ai")
    monkeypatch.setenv("MYSQL_USER", "user")
    monkeypatch.setenv("MYSQL_PASSWORD", "pass")
    monkeypatch.setenv("TIGER_AI_GATEWAY_URL", "https://example.com")
    monkeypatch.setenv("TIGER_AI_GATEWAY_API_KEY", "key")
    monkeypatch.setenv("TIGER_AI_GATEWAY_MODEL", "model")
    config._settings = None

    settings = get_settings()
    assert settings.mysql_database == "agentic_ai"
    assert settings.tiger_ai_gateway_url == "https://example.com"
