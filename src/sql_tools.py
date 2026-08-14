from __future__ import annotations

from mysql.connector import Error, connect

from .config import settings
from .safety import validate_sql


class SqlExecutionError(Exception):
    pass


def get_connection():
    try:
        return connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database,
        )
    except Error as exc:
        raise SqlExecutionError(
            f"Unable to connect to MySQL database: {exc}"
        )


def run_select(sql: str) -> list[dict]:
    cleaned_sql = validate_sql(sql)

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(cleaned_sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Error as exc:
        raise SqlExecutionError(
            f"Database query failed: {exc}"
        )
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Error:
                pass
        if connection is not None:
            try:
                connection.close()
            except Error:
                pass


def check_database_connection() -> bool:
    connection = None
    try:
        connection = get_connection()
        return True
    finally:
        if connection is not None:
            try:
                connection.close()
            except Error:
                pass
