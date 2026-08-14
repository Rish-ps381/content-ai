from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from mysql.connector import connect, Error

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TABLE_FILES = {
    "customers.csv": "customers",
    "products.csv": "products",
    "stores.csv": "stores",
    "sales_transactions.csv": "sales_transactions",
    "returns.csv": "returns",
}

REQUIRED_ENV_VARS = [
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DATABASE",
]


def load_environment() -> None:
    load_dotenv()

    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}."
            " Set them in your environment or in a .env file."
        )


def get_connection() -> "mysql.connector.connection.MySQLConnection":
    try:
        connection = connect(
            host=os.environ["MYSQL_HOST"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            autocommit=False,
        )
        return connection
    except Error as exc:
        raise ConnectionError(
            f"Failed to connect to MySQL: {exc}."
            " Check your MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE settings."
        )


def read_csv_file(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        raise RuntimeError(f"Unable to read CSV file {csv_path}: {exc}")

    return df


def insert_table_rows(connection, table_name: str, dataframe: pd.DataFrame) -> int:
    if dataframe.empty:
        print(f"No rows to load for {table_name}. Skipping.")
        return 0

    columns = list(dataframe.columns)
    quoted_columns = ", ".join(f"`{col}`" for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    update_clause = ", ".join(f"`{col}` = VALUES(`{col}`)" for col in columns)

    insert_sql = (
        f"INSERT INTO `{table_name}` ({quoted_columns})"
        f" VALUES ({placeholders})"
        f" ON DUPLICATE KEY UPDATE {update_clause}"
    )

    values = [tuple(None if pd.isna(v) else v for v in row) for row in dataframe.itertuples(index=False, name=None)]

    try:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, values)
        connection.commit()
    except Error as exc:
        connection.rollback()
        raise RuntimeError(f"Failed to load data into {table_name}: {exc}")

    return len(values)


def load_all_tables() -> None:
    load_environment()
    connection = get_connection()

    try:
        for csv_name, table_name in TABLE_FILES.items():
            csv_path = DATA_DIR / csv_name
            print(f"Loading {csv_name} into {table_name}...")
            df = read_csv_file(csv_path)
            row_count = insert_table_rows(connection, table_name, df)
            print(f"Loaded {row_count} rows into {table_name}.")
    finally:
        connection.close()


if __name__ == "__main__":
    try:
        load_all_tables()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
