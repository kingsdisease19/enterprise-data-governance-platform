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

# --- Data Quality Rules (from docs/data-quality-rules.md) ---
QUALITY_RULES = [
    ("BANK-001", "bank.csv", "Validity", "balance should not be negative", "High"),
    ("BANK-004", "bank.csv", "Completeness", "job must not be null/blank", "Medium"),
    ("BANK-005", "bank.csv", "Uniqueness", "no fully duplicate rows", "Medium"),
    ("CHURN-001", "Churn_Modelling.csv", "Uniqueness", "CustomerId must be unique", "Critical"),
    ("CHURN-002", "Churn_Modelling.csv", "Validity", "Balance must not be negative", "High"),
    ("CHURN-005", "Churn_Modelling.csv", "Completeness", "Geography must not be null/blank", "Medium"),
    ("CHURN-007", "Churn_Modelling.csv", "Consistency", "Geography must be a known country", "Low"),
    ("HR-001", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Uniqueness", "EmployeeNumber must be unique", "Critical"),
    ("HR-002", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Validity", "MonthlyIncome must be greater than 0", "High"),
    ("HR-004", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Completeness", "Attrition must not be null", "Medium"),
    ("HR-007", "WA_Fn-UseC_-HR-Employee-Attrition.csv", "Consistency", "Attrition must be Yes or No", "Low"),
    ("LOAN-001", "Bank_Personal_Loan_Modelling.xlsx", "Uniqueness", "ID must be unique", "Critical"),
    ("LOAN-002", "Bank_Personal_Loan_Modelling.xlsx", "Validity", "Experience must not be negative", "High"),
    ("LOAN-003", "Bank_Personal_Loan_Modelling.xlsx", "Completeness", "Income must not be null", "High"),
    ("LOAN-007", "Bank_Personal_Loan_Modelling.xlsx", "Consistency", "Education must be 1, 2, or 3", "Low"),
]

# --- Policy-to-Asset Links (which assets each policy governs) ---
# Format: (policy_name, [list of asset_names it applies to])
POLICY_LINKS = [
    ("PII Access Restriction", [
        "Retail Customer Register", "Employee Records", "Personal Loan & Product Holdings"
    ]),
    ("Raw Data Immutability", [
        "Bank Customer Contact Register", "Bank Account & Balance Records", "Retail Customer Register",
        "Customer Churn Status", "Employee Records", "Employee Attrition & Performance Data",
        "Personal Loan & Product Holdings"
    ]),
    ("Quality Rule Enforcement", [
        "Bank Customer Contact Register", "Bank Account & Balance Records", "Retail Customer Register",
        "Customer Churn Status", "Employee Records", "Employee Attrition & Performance Data",
        "Personal Loan & Product Holdings"
    ]),
    ("Ownership Requirement", [
        "Bank Customer Contact Register", "Bank Account & Balance Records", "Retail Customer Register",
        "Customer Churn Status", "Employee Records", "Employee Attrition & Performance Data",
        "Personal Loan & Product Holdings"
    ]),
]

# --- Data Lineage (same 6 stages for every asset, since all datasets follow the same pipeline) ---
LINEAGE_STAGES = [
    (1, "Source", "Original open dataset downloaded from Kaggle"),
    (2, "Raw Storage", "Untouched original file stored in datasets/raw/"),
    (3, "Database Load", "Loaded into PostgreSQL table via load_to_postgres.py"),
    (4, "Quality Check", "Quality rules run via check_data_quality_sql.py, results stored in quality_findings"),
    (5, "Power BI Dashboard", "quality_findings table visualized in Power BI dashboard"),
    (6, "Streamlit Portal", "Governance repository surfaced via Streamlit portal (Sprint 7.5)"),
]

# --- Governance Issues (rebuilt to link directly to asset_id) ---
ISSUES_V2 = [
    ("Bank Account & Balance Records", "688 rows contain a negative balance value", "High", "Open",
     "Confirm with Finance whether overdrafts are valid; investigate source if not"),
    ("Personal Loan & Product Holdings", "52 rows contain a negative Experience value", "High", "Open",
     "Correct or remove invalid records; likely data entry error"),
]


def populate():
    with engine.begin() as conn:
        # Clear existing data so this script can be safely re-run
        conn.execute(text("DELETE FROM policy_asset_links"))
        conn.execute(text("DELETE FROM data_quality_rules"))
        conn.execute(text("DELETE FROM data_dictionary"))
        conn.execute(text("DELETE FROM data_owners"))
        conn.execute(text("DELETE FROM data_stewards"))
        conn.execute(text("DELETE FROM governance_issues"))
        conn.execute(text("DELETE FROM data_lineage"))
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
        policy_ids = {}
        for name, desc, applies_to in POLICIES:
            result = conn.execute(
                text("""
                    INSERT INTO governance_policies (policy_name, description, applies_to)
                    VALUES (:name, :desc, :applies_to)
                    RETURNING policy_id
                """),
                {"name": name, "desc": desc, "applies_to": applies_to}
            )
            policy_ids[name] = result.scalar()
        print(f"Inserted {len(POLICIES)} governance policies")

        # Policy-to-asset links
        link_count = 0
        for policy_name, asset_names in POLICY_LINKS:
            for asset_name in asset_names:
                conn.execute(
                    text("INSERT INTO policy_asset_links (policy_id, asset_id) VALUES (:policy_id, :asset_id)"),
                    {"policy_id": policy_ids[policy_name], "asset_id": asset_ids[asset_name]}
                )
                link_count += 1
        print(f"Inserted {link_count} policy-asset links")

        # Data quality rules
        for rule_id, dataset_name, dimension, desc, severity in QUALITY_RULES:
            conn.execute(
                text("""
                    INSERT INTO data_quality_rules (rule_id, dataset_name, dimension, description, severity)
                    VALUES (:rule_id, :dataset_name, :dimension, :desc, :severity)
                """),
                {"rule_id": rule_id, "dataset_name": dataset_name, "dimension": dimension, "desc": desc, "severity": severity}
            )
        print(f"Inserted {len(QUALITY_RULES)} data quality rules")

        # Governance issues (linked to asset_id)
        for asset_name, desc, severity, status, rec in ISSUES_V2:
            conn.execute(
                text("""
                    INSERT INTO governance_issues (related_asset, asset_id, issue_description, severity, status, recommendation)
                    VALUES (:asset_name, :asset_id, :desc, :severity, :status, :rec)
                """),
                {"asset_name": asset_name, "asset_id": asset_ids[asset_name], "desc": desc,
                 "severity": severity, "status": status, "rec": rec}
            )
        print(f"Inserted {len(ISSUES_V2)} governance issues")

        # Data lineage (same 6 stages applied to every registered asset)
        lineage_count = 0
        for asset_name, asset_id in asset_ids.items():
            for order, stage_name, stage_desc in LINEAGE_STAGES:
                conn.execute(
                    text("""
                        INSERT INTO data_lineage (asset_id, stage_order, stage_name, stage_description)
                        VALUES (:asset_id, :stage_order, :stage_name, :stage_desc)
                    """),
                    {"asset_id": asset_id, "stage_order": order, "stage_name": stage_name, "stage_desc": stage_desc}
                )
                lineage_count += 1
        print(f"Inserted {lineage_count} lineage records")

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