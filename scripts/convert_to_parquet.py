"""Convert messy CSV to Parquet"""

from pathlib import Path
import duckdb

RAW = Path("../data/raw/Compuspections_merge.csv")
OUT = Path("../data/processed/Compuspections_merge.parquet")

con = duckdb.connect()

print("Converting CSV -> Parquet (safe mode)...")

con.execute(f"""
COPY (
    SELECT *
    FROM read_csv_auto(
        '{RAW}',
        all_varchar=true
    )
)
TO '{OUT}'
(FORMAT PARQUET);
""")

print("Done.")
