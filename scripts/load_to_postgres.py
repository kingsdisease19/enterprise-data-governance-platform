"""
load_to_postgres.py

Loads all four raw datasets into the governance_platform PostgreSQL database.
Each dataset becomes its own table.

Usage:
    python scripts/load_to_postgres.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text

# Database configuration from environment variables
DB_USER = "postgres"
DB_PASSWORD = os.environ.get("PG_PASSWORD", "YOUR_PASSWORD_HERE")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "governance_platform"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

datasets = [
    {"table": "bank", "path": "datasets/raw/bank.csv", "sheet": None},
    {"table": "churn_modelling", "path": "datasets/raw/Churn_Modelling.csv", "sheet": None},
    {"table": "hr_attrition", "path": "datasets/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv", "sheet": None},
    {"table": "personal_loan", "path": "datasets/raw/Bank_Personal_Loan_Modelling.xlsx", "sheet": "Data"},
]

for ds in datasets:
    if ds["path"].endswith(".xlsx"):
        df = pd.read_excel(ds["path"], sheet_name=ds["sheet"])
    else:
        df = pd.read_csv(ds["path"])

    df.to_sql(ds["table"], engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into table '{ds['table']}'")

print("All datasets loaded into PostgreSQL.")