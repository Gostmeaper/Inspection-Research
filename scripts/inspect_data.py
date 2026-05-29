"""Main inspection script"""

import duckdb

DB_FILE = "../data/processed/Compuspections_merge.parquet"

con = duckdb.connect()

print("\n=== COLUMN INFO ===")
print(
    con.execute(f"""
    DESCRIBE SELECT * FROM '{DB_FILE}'
    """).fetchdf()
)

print("\n=== ROW COUNT ===")
print(
    con.execute(f"""
    SELECT COUNT(*) AS rows
    FROM '{DB_FILE}'
    """).fetchdf()
)

print("\n=== SAMPLE ROWS ===")
print(
    con.execute(f"""
    SELECT *
    FROM '{DB_FILE}'
    LIMIT 10
    """).fetchdf()
)
