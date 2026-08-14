# AI Usage Log

This document records how GitHub Copilot assisted during the assignment and how the learner reviewed the generated work.

## 1. Dataset/schema inspection
- Purpose: Understand the retail CSV schema and ensure the SQL queries match the data.
- AI assistance used: Copilot reviewed the `data/` files and helped identify schema fields from `database/mysql_schema.sql` and the CSV loader.
- Human review performed: The learner confirmed field names and data relationships by reading schema and CSV-related code.

## 2. Project structure
- Purpose: Map the repository layout and locate key modules for the agent.
- AI assistance used: Copilot inspected `src/`, `tests/`, `database/`, and `outputs/` folders.
- Human review performed: The learner validated directory contents and confirmed that important files were present.

## 3. MySQL schema
- Purpose: Verify the retail database tables and columns before generating SQL.
- AI assistance used: Copilot read `database/mysql_schema.sql` and inferred required tables and keys.
- Human review performed: The learner reviewed the schema file and confirmed table definitions.

## 4. Data loader
- Purpose: Validate how CSV files are loaded into MySQL and ensure the loader matches table structure.
- AI assistance used: Copilot inspected `database/load_data.py` and confirmed the CSV-to-table mapping.
- Human review performed: The learner reviewed the loader logic, environment requirements, and row insertion behavior.

## 5. Configuration
- Purpose: Ensure environment variables are loaded safely and avoid hardcoded credentials.
- AI assistance used: Copilot inspected `src/config.py` and `.env.example` handling.
- Human review performed: The learner confirmed lazy settings loading and documented required variables.

## 6. LLM client
- Purpose: Verify how LLM requests are built and sent to the configured gateway.
- AI assistance used: Copilot reviewed `src/tiger_gateway_client.py` and its request/response handling.
- Human review performed: The learner validated the HTTP payload structure, error handling, and API configuration.

## 7. SQL safety
- Purpose: Make sure destructive SQL is blocked and only safe SELECT queries are allowed.
- AI assistance used: Copilot reviewed `src/safety.py` and helped define safety test cases.
- Human review performed: The learner verified the validator logic and confirmed blocking of forbidden keywords and multiple statements.

## 8. MySQL tool
- Purpose: Validate the actual query executor and safe connection handling.
- AI assistance used: Copilot inspected `src/sql_tools.py` and its connection/cleanup logic.
- Human review performed: The learner confirmed the safe query execution path and exception handling.

## 9. Memory
- Purpose: Confirm that follow-up questions can be supported with recent conversation history.
- AI assistance used: Copilot reviewed `src/memory.py` and memory usage in `src/graph.py` and `src/app.py`.
- Human review performed: The learner validated memory storage, retrieval, and prompt formatting behavior.

## 10. LangGraph workflow
- Purpose: Verify the end-to-end workflow from user input to answer generation.
- AI assistance used: Copilot reviewed `src/graph.py` and the use of a state graph to sequence SQL generation, validation, query execution, and summarization.
- Human review performed: The learner confirmed the workflow steps and the compiled graph execution path.

## 11. CLI
- Purpose: Validate the interactive command-line entrypoint for the agent.
- AI assistance used: Copilot reviewed `src/app.py` and the main loop.
- Human review performed: The learner confirmed input handling, schema loading, result printing, and error handling.

## 12. Tests
- Purpose: Ensure deterministic pytest coverage for safety, memory, graph workflow, and configuration.
- AI assistance used: Copilot created and updated test files in `tests/`, including `test_agent.py` and `test_memory.py`.
- Human review performed: The learner ran `pytest`, reviewed failures, and confirmed all tests passed.

## 13. Debugging
- Purpose: Resolve issues in command execution, environment handling, and script generation.
- AI assistance used: Copilot suggested inspecting file contents, fixing shell command quoting, and running targeted tests.
- Human review performed: The learner manually verified commands, reviewed terminal output, and corrected the workflow as needed.

## 14. Documentation
- Purpose: Create a complete README and supporting evidence artifacts.
- AI assistance used: Copilot drafted `README.md`, `requirements.txt`, and validation summaries.
- Human review performed: The learner read and edited the documentation for accuracy and consistency.

## 15. Evaluation test cases
- Purpose: Create structured evaluation artifacts for real and safety test cases.
- AI assistance used: Copilot generated `outputs/test_case_results.csv` and `outputs/sql_safety_summary.csv`.
- Human review performed: The learner confirmed the CSV contents and ensured actual validation results were used where available.

## Review statement
All generated code and documentation were reviewed by the learner. The learner validated implementation behavior using tests, file inspection, and actual execution evidence where possible.