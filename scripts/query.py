"""Analytics script"""

import duckdb

DB_FILE = "../data/processed/TruckInspection_score5.parquet"

con = duckdb.connect()

query = f"""
SELECT *
FROM '{DB_FILE}'
LIMIT 20
"""

result = con.execute(query).fetchdf()

print(result)