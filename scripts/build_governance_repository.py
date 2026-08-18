"""
build_governance_repository.py

Populates the governance repository tables in PostgreSQL using the
governance artifacts already created in earlier sprints (data asset
inventory, data dictionary, business glossary, metadata, quality rules).

Usage:
    set PG_PASSWORD=your_actual_password
    python scripts/build_governance_repository.py
"""

import os
from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = os.environ.get("PG_PASSWORD", "YOUR_PASSWORD_HERE")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "governance_platform"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- Data Assets (from docs/data-asset-inventory.md) ---
DATA_ASSETS = [
    ("Bank Customer Contact Register", "Demographic and marketing contact data", "bank.csv", "Confidential", "Medium"),
    ("Bank Account & Balance Records", "Customer balance and loan/housing status", "bank.csv", "Confidential", "High"),
    ("Retail Customer Register", "Customer identity, geography, tenure", "Churn_Modelling.csv", "Confidential", "High"),
    ("Customer Churn Status", "Whether a customer exited the bank", "Churn_Modelling.csv", "Internal", "Medium"),
    ("Employee Records", "Employee demographics, role, compensation", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Restricted", "High"),
    ("Employee Attrition & Performance Data", "Attrition flag, satisfaction, performance", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Confidential", "Medium"),
    ("Personal Loan & Product Holdings", "Income, credit behavior, product uptake", "Bank_Personal_Loan_Modelling.xlsx", "Confidential", "High"),
]

# --- Business Glossary (from docs/business-glossary.md) ---
GLOSSARY = [
    ("Customer", "An individual who holds one or more accounts or products with the organization"),
    ("Balance", "The current amount of money held in a customer's account at a given point in time"),
    ("Loan", "Money borrowed by a customer from the organization, to be repaid with interest"),
    ("Attrition", "When an employee voluntarily or involuntarily leaves the organization"),
    ("Customer Churn", "When a customer closes their accounts and stops using the organization's services"),
    ("Salary", "Fixed regular compensation paid to an employee, usually stated monthly or annually"),
    ("Experience", "The number of years an individual has spent in professional employment"),
    ("Credit Score", "A numerical rating of a customer's creditworthiness, used to assess lending risk"),
    ("Term Deposit", "A savings product where money is deposited for a fixed period in exchange for interest"),
    ("Active Member", "A customer who has used the organization's products/services within a recent, defined period"),
]

# --- Governance Policies (new for this sprint) ---
POLICIES = [
    ("PII Access Restriction", "Personally identifiable fields (names, salaries, income) may only be accessed by authorized roles", "Confidential/Restricted assets"),
    ("Raw Data Immutability", "Raw source files must never be edited directly; all changes happen on processed copies", "All datasets"),
    ("Quality Rule Enforcement", "Every registered dataset must have at least one documented quality rule per dimension where applicable", "All datasets"),
    ("Ownership Requirement", "Every registered data asset must have an assigned Data Owner and Data Steward", "All datasets"),
]

# --- Governance Issues (derived from real quality findings) ---
ISSUES = [
    ("bank.csv - balance", "688 rows contain a negative balance value", "High", "Open", "Confirm with Finance whether overdrafts are valid; investigate source if not"),
    ("Bank_Personal_Loan_Modelling.xlsx - Experience", "52 rows contain a negative Experience value", "High", "Open", "Correct or remove invalid records; likely data entry error"),
]

# --- Data Owners & Stewards (linked by asset name, resolved to asset_id at insert time) ---
OWNERS = [
    ("Bank Customer Contact Register", "Marketing Director", "Marketing"),
    ("Bank Account & Balance Records", "Head of Finance", "Finance"),
    ("Retail Customer Register", "Head of Retail Banking", "Retail Banking"),
    ("Customer Churn Status", "Head of Customer Analytics", "Retail Banking"),
    ("Employee Records", "HR Director", "Human Resources"),
    ("Employee Attrition & Performance Data", "HR Analytics Manager", "Human Resources"),
    ("Personal Loan & Product Holdings", "Head of Lending", "Lending"),
]

STEWARDS = [
    ("Bank Customer Contact Register", "Marketing Analyst", "Marketing"),
    ("Bank Account & Balance Records", "Finance Data Steward", "Finance"),
    ("Retail Customer Register", "Customer Data Steward", "Retail Banking"),
    ("Customer Churn Status", "Customer Analytics Steward", "Retail Banking"),
    ("Employee Records", "HR Data Steward", "Human Resources"),
    ("Employee Attrition & Performance Data", "HR Analytics Steward", "Human Resources"),
    ("Personal Loan & Product Holdings", "Lending Data Steward", "Lending"),
]


def populate():
    with engine.begin() as conn:
        # Clear existing data so this script can be safely re-run
        conn.execute(text("DELETE FROM data_owners"))
        conn.execute(text("DELETE FROM data_stewards"))
        conn.execute(text("DELETE FROM governance_issues"))
        conn.execute(text("DELETE FROM governance_policies"))
        conn.execute(text("DELETE FROM business_glossary"))
        conn.execute(text("DELETE FROM data_assets"))
        print("Cleared existing governance repository data")

        # Data assets
        asset_ids = {}
        for name, desc, source, classification, criticality in DATA_ASSETS:
            result = conn.execute(
                text("""
                    INSERT INTO data_assets (asset_name, description, source_file, classification, criticality)
                    VALUES (:name, :desc, :source, :classification, :criticality)
                    RETURNING asset_id
                """),
                {"name": name, "desc": desc, "source": source, "classification": classification, "criticality": criticality}
            )
            asset_ids[name] = result.scalar()
        print(f"Inserted {len(DATA_ASSETS)} data assets")

        # Business glossary
        for term, definition in GLOSSARY:
            conn.execute(
                text("INSERT INTO business_glossary (term, definition) VALUES (:term, :definition)"),
                {"term": term, "definition": definition}
            )
        print(f"Inserted {len(GLOSSARY)} glossary terms")

        # Governance policies
        for name, desc, applies_to in POLICIES:
            conn.execute(
                text("INSERT INTO governance_policies (policy_name, description, applies_to) VALUES (:name, :desc, :applies_to)"),
                {"name": name, "desc": desc, "applies_to": applies_to}
            )
        print(f"Inserted {len(POLICIES)} governance policies")

        # Governance issues
        for asset, desc, severity, status, rec in ISSUES:
            conn.execute(
                text("""
                    INSERT INTO governance_issues (related_asset, issue_description, severity, status, recommendation)
                    VALUES (:asset, :desc, :severity, :status, :rec)
                """),
                {"asset": asset, "desc": desc, "severity": severity, "status": status, "rec": rec}
            )
        print(f"Inserted {len(ISSUES)} governance issues")

        # Data owners
        for asset_name, owner_name, department in OWNERS:
            conn.execute(
                text("""
                    INSERT INTO data_owners (asset_id, owner_name, department)
                    VALUES (:asset_id, :owner_name, :department)
                """),
                {"asset_id": asset_ids[asset_name], "owner_name": owner_name, "department": department}
            )
        print(f"Inserted {len(OWNERS)} data owners")

        # Data stewards
        for asset_name, steward_name, department in STEWARDS:
            conn.execute(
                text("""
                    INSERT INTO data_stewards (asset_id, steward_name, department)
                    VALUES (:asset_id, :steward_name, :department)
                """),
                {"asset_id": asset_ids[asset_name], "steward_name": steward_name, "department": department}
            )
        print(f"Inserted {len(STEWARDS)} data stewards")


if __name__ == "__main__":
    populate()
    print("Governance repository populated successfully.")