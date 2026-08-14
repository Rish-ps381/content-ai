# Natural Language SQL Data Agent

## Purpose

This project is a retail-focused natural language SQL data agent. It lets business users ask questions in plain English and receive grounded answers from a MySQL retail dataset, while enforcing query safety and preserving conversational follow-up context.

## Architecture

- **User question**: The user asks a natural-language business question.
- **LangGraph**: `src/graph.py` orchestrates the pipeline as a state graph.
- **SQL generation**: The agent builds an LLM prompt and generates a single MySQL `SELECT` statement.
- **SQL safety**: `src/safety.py` validates the generated SQL and blocks destructive or non-SELECT queries.
- **MySQL**: `src/sql_tools.py` executes the safe query against the configured MySQL database.
- **Result summarization**: The agent uses the returned rows to produce a concise business answer grounded in the query result.
- **Memory**: `src/memory.py` stores recent exchanges so follow-up questions can reference prior context.
- **Answer**: The final response is delivered as a business summary grounded in SQL results.

## Project structure

- `src/` - core application modules
  - `src/app.py` - CLI entrypoint for the agent
  - `src/graph.py` - LangGraph workflow implementation
  - `src/safety.py` - SQL safety validator
  - `src/sql_tools.py` - MySQL SELECT executor
  - `src/memory.py` - conversation memory
  - `src/config.py` - environment configuration loader
  - `src/tiger_gateway_client.py` - LLM gateway client
- `database/` - schema and data loading helpers
  - `database/mysql_schema.sql` - MySQL schema for the retail dataset
  - `database/load_data.py` - CSV loader into MySQL
- `data/` - source CSV files
- `tests/` - pytest coverage for safety, memory, graph, and workflow logic
- `outputs/` - generated validation artifacts and summaries
- `.env.example` - environment variable template

## Prerequisites

- Python 3.11+ (compatible with the project imports)
- MySQL server
- MySQL Workbench or another MySQL client for database inspection
- An approved LLM/API endpoint compatible with the Tiger gateway pattern

## Windows PowerShell setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## MySQL setup

1. Create the database and schema:
   - Open MySQL Workbench or another MySQL client.
   - Run the SQL statements in `database/mysql_schema.sql`.

2. Load CSV data:
   - Configure MySQL credentials in a `.env` file based on `.env.example`.
   - Run:
     ```powershell
     python database/load_data.py
     ```
   - This script loads `customers.csv`, `products.csv`, `stores.csv`, `sales_transactions.csv`, and `returns.csv` into the matching tables.

## Environment variables

Copy `.env.example` to `.env` and set values for:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `TIGER_AI_GATEWAY_URL`
- `TIGER_AI_GATEWAY_API_KEY`
- `TIGER_AI_GATEWAY_MODEL`

Do not commit real credentials to source control.

## Running the application

```powershell
python src/app.py
```

## Running tests

```powershell
pytest
```

## Example questions

- What is the total sales revenue for the current dataset?
- Show revenue by store region.
- List the top 5 customers by revenue.
- Provide a revenue breakdown by product category.
- How many returns were processed in total?

## SQL safety

This project enforces strict SQL safety. Only `SELECT` and `WITH`/CTE-based queries are allowed. Any query containing `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `REPLACE`, or multiple statements is rejected.

## Conversation memory

The agent stores recent exchanges in `src/memory.py`. Follow-up questions can reference prior user prompts and assistant messages so the agent can preserve context across a conversation.

## Validation

- A set of 10 evaluation cases was created in `outputs/test_case_results.csv`.
- SQL safety behavior is recorded in `outputs/sql_safety_summary.csv`.
- The pytest test suite covers the safety validator, memory, graph workflow, and application logic.

## Responsible AI

- The project is designed for synthetic retail data only.
- No real credentials are committed to the repository.
- Generated SQL and business answers should be reviewed by a human.
- Answers are intended to be grounded only in SQL results returned by the database.