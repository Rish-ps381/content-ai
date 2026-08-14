from pathlib import Path
from src.safety import validate_sql

cases = [
    (1, 'SELECT * FROM stores', 'Allowed'),
    (2, 'INSERT INTO stores (store_id, city) VALUES ("S1", "City")', 'Blocked'),
    (3, 'UPDATE stores SET city = "Delhi" WHERE store_id = "S1"', 'Blocked'),
    (4, 'DELETE FROM stores WHERE store_id = "S1"', 'Blocked'),
    (5, 'DROP TABLE stores', 'Blocked'),
    (6, 'ALTER TABLE stores ADD COLUMN region_code VARCHAR(10)', 'Blocked'),
    (7, 'TRUNCATE TABLE stores', 'Blocked'),
    (8, 'CREATE TABLE test (id INT)', 'Blocked'),
    (9, 'REPLACE INTO stores (store_id, city) VALUES ("S1", "City")', 'Blocked'),
    (10, 'SELECT * FROM stores; DROP TABLE stores', 'Blocked'),
]

path = Path('outputs/sql_safety_summary.csv')
path.parent.mkdir(parents=True, exist_ok=True)
with path.open('w', encoding='utf-8') as f:
    f.write('test_id,sql,expected,actual,pass_fail\n')
    for test_id, sql, expected in cases:
        try:
            validate_sql(sql)
            actual = 'Allowed'
            pass_fail = 'PASS' if expected == 'Allowed' else 'FAIL'
        except Exception as exc:
            actual = f'{type(exc).__name__}: {exc}'
            pass_fail = 'PASS' if expected == 'Blocked' else 'FAIL'
        safe_sql = sql.replace('"', '""')
        safe_actual = actual.replace(',', ';')
        f.write(f'{test_id},"{safe_sql}",{expected},"{safe_actual}",{pass_fail}\n')
print('wrote', path)
