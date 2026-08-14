# Human Review Notes

This document summarizes the human-in-the-loop validation performed during the project.

## CSV schema verification
- Verified the CSV-to-table mapping by inspecting `database/load_data.py` and `database/mysql_schema.sql`.
- Confirmed that the five retail CSV files are expected to load into `customers`, `products`, `stores`, `sales_transactions`, and `returns`.
- Actual CSV row values were not exhaustively validated against the schema in this run.

## MySQL table verification
- Reviewed `database/mysql_schema.sql` for table definitions and foreign keys.
- Attempted MySQL connectivity from the workspace, but local database access failed due to missing credentials in the current environment.
- Confirmed that MySQL validation could not complete because `root` and anonymous connection attempts were denied.
- Actual table creation and table contents were not confirmed in a live database during this session.

## Row-count verification
- The project includes a CSV loader that loads rows into MySQL tables.
- No live row counts were collected because MySQL access was unavailable.
- Row-counts need verification once valid database credentials are available.

## SQL safety testing
- Reviewed `src/safety.py` logic for blocking destructive and non-SELECT queries.
- Executed safety test cases and generated `outputs/sql_safety_summary.csv` with actual validator results.
- Confirmed the validator rejects `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `REPLACE`, and multiple-statement SQL.

## Generated SQL review
- Verified the intended SQL generation flow in `src/graph.py` and `src/tiger_gateway_client.py`.
- Confirmed prompt structure intends to produce a single safe MySQL `SELECT` query using schema and history.
- Actual generated SQL from the live LLM was not validated in this session because no LLM gateway was configured.

## Business-answer grounding
- Reviewed the summarization step in `src/graph.py`, which asks the LLM to produce answers grounded only in returned rows.
- Confirmed the design intention to avoid inventing facts beyond SQL results.
- Ground truth business-answer validation against actual SQL output is pending a live query run.

## Follow-up memory testing
- Validated memory behavior in tests such as `tests/test_memory.py` and `tests/test_agent.py`.
- Confirmed `ConversationMemory` stores user questions, assistant answers, and generated SQL.
- Confirmed `get_recent_messages()` returns role-labeled history for follow-up prompts.
- A full end-to-end follow-up execution with the live workflow was not performed.

## No-data handling
- Reviewed `src/graph.py` logic for returning "The query returned no results." when no rows are returned.
- Confirmed this no-data handling is implemented in the summarization step.
- No-data behavior was not validated with a live database query in this session.

## Error handling
- Reviewed application error handling in `src/app.py`, including safety errors and LLM gateway errors.
- Reviewed MySQL execution error handling in `src/sql_tools.py` and data loader error handling in `database/load_data.py`.
- Confirmed exceptions are surfaced and database resources are closed safely.

## Credential/security review
- Verified that `.env.example` is provided and no real credentials are committed.
- Confirmed `src/config.py` reads credentials from environment variables and `.env` only.
- Confirmed the README and evidence logs note the requirement to keep credentials out of source control.

## pytest execution
- Executed the full pytest suite successfully: `38 passed`.
- Verified coverage includes safety, memory, graph workflow, and configuration behavior.

## 10 test-case evaluation
- Created `outputs/test_case_results.csv` with 10 evaluation cases for business questions and destructive SQL safety.
- Confirmed the file was generated and contains expected behavior and safety outcomes.
- Actual execution of those 10 evaluation cases against a live database and live agent was not completed due to unavailable database/LLM configuration.

## Review summary
- Generated code and artifacts were reviewed by the learner.
- The learner validated tests and static code behavior where possible.
