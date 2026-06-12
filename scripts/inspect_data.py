"""Main inspection script"""

import duckdb
import pandas as pd

DB_FILE = "../data/processed/TruckInspection_score5.parquet"

con = duckdb.connect()

# ── Column inventory ──────────────────────────────────────────────────────────
desc = con.execute(f"DESCRIBE SELECT * FROM '{DB_FILE}'").fetchdf()
total_cols = len(desc)

print(f"\n=== COLUMN INVENTORY ({total_cols} total) ===")

# Group columns by prefix so 481 columns are readable
GROUPS = {
    "Metadata":        desc["column_name"].str.match(r"^(StartDate|EndDate|Status|IPAddress|Progress|Duration|Finished|RecordedDate|ResponseId|Recipient|External|Location|Distribution|UserLanguage|Q_Recaptcha)"),
    "Demographics":    desc["column_name"].str.match(r"^(Q5|Q7|Q8|Q9|Q11|Q37)"),
    "Decision factors (Q)": desc["column_name"].str.match(r"^Q\d"),
    "File upload":     desc["column_name"].str.match(r"^Q118"),
    "Inspection results (BxRes)":  desc["column_name"].str.match(r"^B\dRes_"),
    "Inspect button (BxYbtn)":     desc["column_name"].str.match(r"^B\dybtn_"),
    "No-inspect button (BxNbtn)":  desc["column_name"].str.match(r"^B\dnbtn_"),
    "Loop IDs":        desc["column_name"].str.match(r"^B\dloopId_"),
    "Vehicle vars":    desc["column_name"].str.match(r"^var\d"),
    "S-response":      desc["column_name"].str.match(r"^B\dsresponse_"),
    "Sybtn / Snbtn":   desc["column_name"].str.match(r"^B\ds[yn]btn_"),
    "Ground truth":    desc["column_name"].str.match(r"^tybtn_"),
    "Scores":          desc["column_name"].str.match(r"^(score|total_score|hide|resp\d)"),
    "Trial count":     desc["column_name"].str.match(r"^n_trial"),
}

accounted = set()
for group, mask in GROUPS.items():
    cols = desc.loc[mask, "column_name"].tolist()
    accounted.update(cols)
    if cols:
        print(f"  {group:35s} {len(cols):3d}  e.g. {cols[0]}")

leftover = [c for c in desc["column_name"] if c not in accounted]
if leftover:
    print(f"  {'Other':35s} {len(leftover):3d}  {leftover}")

# ── Row count ─────────────────────────────────────────────────────────────────
print("\n=== ROW COUNT ===")
print(con.execute(f"SELECT COUNT(*) AS rows FROM '{DB_FILE}'").fetchdf().to_string(index=False))

# ── Sample: metadata + key decision columns only ──────────────────────────────
print("\n=== SAMPLE ROWS (metadata + round-1 decisions) ===")
sample_cols = [
    "ResponseId", "StartDate", "Duration (in seconds)", "Finished",
    "Q9",           # job title
    "Q2-round1",    # factors round 1
    "B1ybtn_1", "B1ybtn_2", "B1ybtn_3", "B1ybtn_4",
    "B1ybtn_5", "B1ybtn_6", "B1ybtn_7", "B1ybtn_8",
    "total_score1", "total_score2", "total_score3", "total_score4", "total_score5",
]
# Only keep cols that exist in this file
available = set(desc["column_name"])
select_cols = ", ".join(f'"{c}"' for c in sample_cols if c in available)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 30)

print(con.execute(f"SELECT {select_cols} FROM '{DB_FILE}' LIMIT 10").fetchdf().to_string(index=False))
