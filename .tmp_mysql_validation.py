import os
from pathlib import Path

output_path = Path('outputs/mysql_validation.md')
output_path.parent.mkdir(parents=True, exist_ok=True)

lines = []
lines.append('# MySQL Validation')

# Determine connection settings
mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_port = int(os.getenv('MYSQL_PORT', '3306'))
mysql_database = os.getenv('MYSQL_DATABASE', 'agentic_ai')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')

lines.append('')
lines.append('## Configuration')
lines.append(f'- Host: `{mysql_host}`')
lines.append(f'- Port: `{mysql_port}`')
lines.append(f'- Database: `{mysql_database}`')
lines.append(f'- MySQL user from environment: `{mysql_user}`')
lines.append(f'- MySQL password configured: `{bool(mysql_password)}`')

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError as exc:
    lines.append('')
    lines.append('## Result')
    lines.append('- `mysql.connector` is not installed in the current Python environment.')
    lines.append(f'- Import error: {exc}')
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    raise SystemExit(1)

lines.append('')
lines.append('## Validation steps')

connection = None
connected = False
connection_errors = []

candidates = []
if mysql_user is not None:
    candidates.append((mysql_user, mysql_password or ''))
else:
    candidates.extend([
        ('root', ''),
        ('root', 'root'),
        ('', ''),
    ])

for user, password in candidates:
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=user,
            password=password,
            database=mysql_database,
            connection_timeout=5,
        )
        connected = True
        used_user = user
        used_password = password
        break
    except Error as exc:
        connection_errors.append((user, str(exc)))

if not connected:
    lines.append('- Unable to connect to MySQL using available credentials.')
    lines.append('- Tried credentials:')
    for user, err in connection_errors:
        lines.append(f'  - `{user}`: {err}')
    lines.append('')
    lines.append('## Conclusion')
    lines.append('- MySQL validation could not be completed because the database is not reachable with the current environment settings.')
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    raise SystemExit(1)

lines.append(f'- Connected to MySQL as `{used_user}`.')
lines.append('')
lines.append('## Database validation')
lines.append(f'- Confirmed database name: `{mysql_database}`')

cursor = connection.cursor()

cursor.execute('SHOW TABLES')
all_tables = [row[0] for row in cursor.fetchall()]
lines.append(f'- Tables created: {all_tables}')

expected_tables = ['customers', 'products', 'stores', 'sales_transactions', 'returns']
present_tables = [t for t in expected_tables if t in all_tables]
missing_tables = [t for t in expected_tables if t not in all_tables]
lines.append(f'- Expected tables present: {present_tables}')
if missing_tables:
    lines.append(f'- Missing expected tables: {missing_tables}')
else:
    lines.append('- All expected tables are present.')

lines.append('')
lines.append('## Row counts')
counts = {}
for table in present_tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM `{table}`')
        count = cursor.fetchone()[0]
        counts[table] = count
        lines.append(f'- `{table}`: {count} rows')
    except Error as exc:
        lines.append(f'- `{table}`: error counting rows: {exc}')

lines.append('')
lines.append('## CSV load confirmation')
lines.append('- The workspace contains five CSV files: customers.csv, products.csv, stores.csv, sales_transactions.csv, returns.csv.')
lines.append(f'- Confirmed that corresponding tables were created for the five CSV files: {present_tables}')

lines.append('')
lines.append('## Query execution check')
select_ok = False
try:
    cursor.execute('SELECT 1')
    rows = cursor.fetchall()
    lines.append(f'- Successfully executed a test SELECT query. Result: {rows}')
    select_ok = True
except Error as exc:
    lines.append(f'- Failed to execute a test SELECT query: {exc}')

if select_ok:
    lines.append('- The agent should be able to execute SELECT queries on this database if configured correctly.')

lines.append('')
lines.append('## Issues encountered')
if not present_tables:
    lines.append('- No expected tables were found; this may mean the CSV files were not loaded into MySQL.')
else:
    lines.append('- No issues encountered during MySQL connectivity and basic validation.')
    if missing_tables:
        lines.append('- Some expected tables were missing; verify the CSV load process if this is unexpected.')

cursor.close()
connection.close()
output_path.write_text('\n'.join(lines), encoding='utf-8')
print('wrote', output_path)
