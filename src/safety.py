from __future__ import annotations

import re

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|REPLACE)\b",
    re.IGNORECASE,
)
LINE_COMMENT = re.compile(r"--.*?$", re.MULTILINE)
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def _remove_comments(sql: str) -> str:
    sql = BLOCK_COMMENT.sub(" ", sql)
    sql = LINE_COMMENT.sub(" ", sql)
    return sql


def validate_sql(sql: str) -> str:
    if sql is None:
        raise ValueError("SQL statement must be a non-empty string.")

    clean_sql = sql.strip()
    if not clean_sql:
        raise ValueError("SQL statement is empty.")

    if clean_sql.endswith(";"):
        clean_sql = clean_sql[:-1].rstrip()

    if ";" in clean_sql:
        raise ValueError("Multiple SQL statements are not allowed.")

    normalized_sql = _remove_comments(clean_sql).strip()
    if not normalized_sql:
        raise ValueError("SQL statement is empty after removing comments.")

    if FORBIDDEN_KEYWORDS.search(normalized_sql):
        raise ValueError("Only SELECT statements are allowed; forbidden SQL keywords were detected.")

    first_token_match = re.match(r"^\s*(\w+)", normalized_sql)
    if not first_token_match:
        raise ValueError("Unable to parse SQL statement.")

    first_token = first_token_match.group(1).upper()
    if first_token not in {"SELECT", "WITH"}:
        raise ValueError("Only SELECT statements are allowed.")

    if first_token == "WITH" and not re.search(r"\bSELECT\b", normalized_sql, re.IGNORECASE):
        raise ValueError("Only SELECT statements are allowed.")

    return clean_sql
