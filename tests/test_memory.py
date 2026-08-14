import pytest

from src.memory import ConversationMemory


def test_add_and_retrieve_exchange():
    memory = ConversationMemory(max_exchanges=5)
    memory.add_exchange(
        user_message="What were total sales last quarter?",
        assistant_message="I found the total sales.",
        generated_sql="SELECT SUM(units_sold * unit_price) FROM sales_transactions;",
    )

    exchanges = memory.get_recent_exchanges()
    assert len(exchanges) == 1
    assert exchanges[0].user_message == "What were total sales last quarter?"
    assert exchanges[0].assistant_message == "I found the total sales."
    assert exchanges[0].generated_sql == "SELECT SUM(units_sold * unit_price) FROM sales_transactions;"

    messages = memory.get_recent_messages()
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert "Generated SQL" in messages[1]["content"]


def test_history_limit():
    memory = ConversationMemory(max_exchanges=2)
    memory.add_exchange("Q1", "A1")
    memory.add_exchange("Q2", "A2")
    memory.add_exchange("Q3", "A3")

    exchanges = memory.get_recent_exchanges()
    assert len(exchanges) == 2
    assert exchanges[0].user_message == "Q2"
    assert exchanges[1].user_message == "Q3"


def test_add_assistant_after_user_message():
    memory = ConversationMemory()
    memory.add_user_message("What city has the highest sales?")
    memory.add_assistant_message(
        "The highest sales are in Jaipur.",
        generated_sql="SELECT city, SUM(units_sold * unit_price) AS revenue FROM sales_transactions GROUP BY city ORDER BY revenue DESC LIMIT 1;",
    )

    exchanges = memory.get_recent_exchanges()
    assert exchanges[0].assistant_message == "The highest sales are in Jaipur."
    assert "SELECT city" in exchanges[0].generated_sql


def test_clear_history():
    memory = ConversationMemory()
    memory.add_exchange("Q", "A")
    memory.clear()
    assert memory.get_recent_exchanges() == []


def test_empty_user_message_raises_value_error():
    memory = ConversationMemory()
    with pytest.raises(ValueError):
        memory.add_user_message("")


def test_add_assistant_without_user_message_raises_error():
    memory = ConversationMemory()
    with pytest.raises(ValueError):
        memory.add_assistant_message("Answer without a question.")
