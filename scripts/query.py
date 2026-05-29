"""Analytics script"""

import duckdb

DB_FILE = "../data/processed/Compuspections_merge.parquet"

con = duckdb.connect()

query = f"""
SELECT *
FROM '{DB_FILE}'
LIMIT 20
"""

result = con.execute(query).fetchdf()

print(result)