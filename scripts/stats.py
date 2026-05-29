"""Fetch Summary and Nulls"""

import duckdb

DB_FILE = "../data/processed/Compuspections_merge.parquet"

con = duckdb.connect()

print("\n=== NULL COUNTS ===")

nulls = con.execute(f"""
SELECT
    COUNT(*) AS total_rows
FROM '{DB_FILE}'
""").fetchdf()

print(nulls)

print("\n=== NUMERIC SUMMARY ===")

summary = con.execute(f"""
SUMMARIZE SELECT * FROM '{DB_FILE}'
""").fetchdf()

print(summary)
