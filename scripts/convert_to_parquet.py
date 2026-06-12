"""Convert messy CSV to Parquet"""

from pathlib import Path
import duckdb

RAW = Path("../data/raw/TruckInspection_score5_completed_merged_Dec10_2025.csv")
OUT = Path("../data/processed/TruckInspection_score5.parquet")

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
