import sqlite3
conn = sqlite3.connect('trust_labs.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
print()

for table in tables:
    table_name = table[0]
    print(f'=== {table_name} ===')
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    for col in columns:
        print(f'  {col[1]} ({col[2]})')
    print()

    # Also show sample data count
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    print(f'  Row count: {count}')
    print()

conn.close()
