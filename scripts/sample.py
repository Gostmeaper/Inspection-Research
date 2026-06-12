"""Random sampling script"""

import duckdb

DB_FILE = "../data/processed/TruckInspection_score5.parquet"

con = duckdb.connect()

sample = con.execute(f"""
SELECT *
FROM '{DB_FILE}'
USING SAMPLE 1000 ROWS
""").fetchdf()

print(sample)
