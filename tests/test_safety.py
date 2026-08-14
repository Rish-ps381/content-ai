import pytest

from src.safety import validate_sql


def test_valid_select():
    assert validate_sql("SELECT * FROM customers") == "SELECT * FROM customers"


def test_select_with_trailing_semicolon():
    assert validate_sql("SELECT * FROM products;") == "SELECT * FROM products"


def test_reject_delete():
    with pytest.raises(ValueError, match="Only SELECT statements are allowed"):
        validate_sql("DELETE FROM customers")


def test_reject_update():
    with pytest.raises(ValueError, match="Only SELECT statements are allowed"):
        validate_sql("UPDATE sales_transactions SET units_sold = 1")


def test_reject_insert():
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql("INSERT INTO customers (customer_id) VALUES ('C-9999')")


def test_reject_drop():
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql("DROP TABLE customers")


def test_reject_alter():
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql("ALTER TABLE stores ADD COLUMN foo VARCHAR(10)")


def test_reject_truncate():
    with pytest.raises(ValueError, match="forbidden SQL keywords"):
        validate_sql("TRUNCATE TABLE sales_transactions")


def test_reject_multiple_statements():
    with pytest.raises(ValueError, match="Multiple SQL statements are not allowed"):
        validate_sql("SELECT * FROM customers; SELECT * FROM products")


def test_reject_empty_sql():
    with pytest.raises(ValueError, match="SQL statement is empty"):
        validate_sql("")
