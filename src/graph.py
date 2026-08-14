from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, TypedDict

from langgraph.graph import StateGraph

from .safety import validate_sql
from .tiger_gateway_client import TigerGatewayClient

SQL_FENCE_PATTERN = re.compile(r"```(?:sql)?\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL)


class GraphState(TypedDict, total=False):
    question: str
    schema_text: str
    recent_history: List[Dict[str, str]]
    sql: str
    rows: List[Dict[str, Any]]
    answer: str


def extract_sql(text: str) -> str:
    if not text or not text.strip():
        raise ValueError("Assistant did not return any SQL.")

    match = SQL_FENCE_PATTERN.search(text)
    sql_text = match.group(1) if match else text
    sql_text = sql_text.strip()

    if sql_text.lower().startswith("sql\n"):
        sql_text = sql_text.split("\n", 1)[1].strip()

    if sql_text.endswith(";"):
        sql_text = sql_text[:-1].rstrip()

    if not sql_text:
        raise ValueError("Could not extract SQL from the assistant response.")

    return sql_text


def format_history_for_prompt(recent_history: List[Dict[str, str]]) -> str:
    if not recent_history:
        return ""

    lines: List[str] = []
    for idx, entry in enumerate(recent_history, start=1):
        role = entry.get("role", "user")
        content = entry.get("content", "")
        if not content:
            continue
        lines.append(f"{idx}. {role.capitalize()}: {content}")
    return "\n".join(lines)


def build_sql_generation_messages(
    question: str,
    schema_text: str,
    recent_history: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are a retail SQL data analyst. Generate exactly one valid MySQL SELECT query. "
                "Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or REPLACE. "
                "Do not produce multiple statements. Return only the SQL or SQL in markdown code fences."
            ),
        },
        {
            "role": "user",
            "content": (
                "Use the retail database schema and recent conversation history to answer the question. "
                "Return only one safe MySQL SELECT statement that retrieves the requested data."
                f"\n\nSchema:\n{schema_text}\n\n"
                f"Recent conversation history (if any):\n{format_history_for_prompt(recent_history) or 'None'}\n\n"
                f"Question: {question}"
            ),
        },
    ]


def build_summary_messages(
    question: str,
    sql: str,
    rows: List[Dict[str, Any]],
) -> List[Dict[str, str]]:
    row_preview = rows[:10]
    return [
        {
            "role": "system",
            "content": (
                "You are a retail data analyst. Give a concise business result that is grounded only in the returned SQL rows. "
                "Do not invent facts or reference data not in the rows."
            ),
        },
        {
            "role": "user",
            "content": (
                "I executed the following SQL query and retrieved these rows. "
                "Provide a short business answer to the original question based strictly on this data."
                f"\n\nQuestion: {question}"
                f"\n\nSQL: {sql}"
                f"\n\nRows: {row_preview}"
                f"\n\nTotal rows returned: {len(rows)}"
            ),
        },
    ]


def create_retail_state_graph(
    client_factory: Callable[[], TigerGatewayClient] = TigerGatewayClient,
    query_runner: Callable[[str], List[Dict[str, Any]]] | None = None,
) -> StateGraph[GraphState, None, GraphState, GraphState]:
    if query_runner is None:
        from .sql_tools import run_select as default_run_select

        query_runner = default_run_select

    graph = StateGraph(GraphState, input_schema=GraphState, output_schema=GraphState)

    def generate_sql_node(state: GraphState) -> GraphState:
        question = state.get("question", "")
        schema_text = state.get("schema_text", "")
        recent_history = state.get("recent_history", [])

        if not question.strip():
            raise ValueError("Question is required for SQL generation.")
        if not schema_text.strip():
            raise ValueError("Database schema text is required for SQL generation.")

        client = client_factory()
        sql = extract_sql(client.send_chat(build_sql_generation_messages(question, schema_text, recent_history)))
        return {"sql": sql}

    def validate_sql_node(state: GraphState) -> GraphState:
        sql = state.get("sql", "")
        return {"sql": validate_sql(sql)}

    def run_query_node(state: GraphState) -> GraphState:
        sql = state.get("sql", "")
        return {"rows": query_runner(sql)}

    def summarize_answer_node(state: GraphState) -> GraphState:
        if not state.get("rows"):
            return {"answer": "The query returned no results."}

        question = state.get("question", "")
        sql = state.get("sql", "")
        rows = state.get("rows", [])
        client = client_factory()
        answer = client.send_chat(build_summary_messages(question, sql, rows))
        return {"answer": answer}

    graph.add_node(generate_sql_node)
    graph.add_node(validate_sql_node)
    graph.add_node(run_query_node)
    graph.add_node(summarize_answer_node)

    graph.set_entry_point("generate_sql_node")
    graph.add_edge("generate_sql_node", "validate_sql_node")
    graph.add_edge("validate_sql_node", "run_query_node")
    graph.add_edge("run_query_node", "summarize_answer_node")
    graph.set_finish_point("summarize_answer_node")

    return graph.compile()


def run_retail_state_graph(
    question: str,
    schema_text: str,
    recent_history: List[Dict[str, str]],
    client_factory: Callable[[], TigerGatewayClient] = TigerGatewayClient,
    query_runner: Callable[[str], List[Dict[str, Any]]] | None = None,
) -> GraphState:
    compiled_graph = create_retail_state_graph(client_factory, query_runner)
    runtime_state: GraphState = {
        "question": question.strip(),
        "schema_text": schema_text.strip(),
        "recent_history": recent_history or [],
    }
    result = compiled_graph.invoke(runtime_state)
    if not isinstance(result, dict):
        raise ValueError("Unexpected graph output format.")
    return result
