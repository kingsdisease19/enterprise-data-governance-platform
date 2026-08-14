"""
check_data_quality_sql.py

Data Governance Platform - SQL-based Data Quality Engine
Runs quality rules as SQL queries directly against PostgreSQL,
scores results by dimension, and writes a findings report.

Usage:
    set PG_PASSWORD=your_actual_password
    python scripts/check_data_quality_sql.py
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

# Each rule: id, dataset/table, dimension, description, severity,
# SQL to count total rows, SQL to count violating rows,
# recommendation shown if the rule fails.
RULES = [
    {
        "id": "BANK-001", "table": "bank", "dimension": "Validity",
        "desc": "balance should not be negative", "severity": "High",
        "violation_sql": "SELECT COUNT(*) FROM bank WHERE balance < 0",
        "recommendation": "Confirm with business whether overdrafts are valid; if not, investigate source system.",
    },
    {
        "id": "BANK-005", "table": "bank", "dimension": "Uniqueness",
        "desc": "no fully duplicate rows", "severity": "Medium",
        "violation_sql": """
            SELECT COALESCE(SUM(cnt),0) FROM (
                SELECT COUNT(*) as cnt FROM bank
                GROUP BY age, job, marital, education, "default", balance,
                         housing, loan, contact, day, month, duration,
                         campaign, pdays, previous, poutcome, deposit
                HAVING COUNT(*) > 1
            ) sub
        """,
        "recommendation": "Investigate source export process for duplicate row generation.",
    },
    {
        "id": "CHURN-001", "table": "churn_modelling", "dimension": "Uniqueness",
        "desc": 'CustomerId must be unique', "severity": "Critical",
        "violation_sql": """
            SELECT COALESCE(SUM(cnt),0) FROM (
                SELECT COUNT(*) as cnt FROM churn_modelling
                GROUP BY "CustomerId" HAVING COUNT(*) > 1
            ) sub
        """,
        "recommendation": "Block downstream reporting until key uniqueness is restored.",
    },
    {
        "id": "CHURN-002", "table": "churn_modelling", "dimension": "Validity",
        "desc": "Balance must not be negative", "severity": "High",
        "violation_sql": 'SELECT COUNT(*) FROM churn_modelling WHERE "Balance" < 0',
        "recommendation": "Investigate source system for negative balance entries.",
    },
    {
        "id": "HR-001", "table": "hr_attrition", "dimension": "Uniqueness",
        "desc": "EmployeeNumber must be unique", "severity": "Critical",
        "violation_sql": """
            SELECT COALESCE(SUM(cnt),0) FROM (
                SELECT COUNT(*) as cnt FROM hr_attrition
                GROUP BY "EmployeeNumber" HAVING COUNT(*) > 1
            ) sub
        """,
        "recommendation": "Block HR reporting until key uniqueness is restored.",
    },
    {
        "id": "HR-002", "table": "hr_attrition", "dimension": "Validity",
        "desc": "MonthlyIncome must be greater than 0", "severity": "High",
        "violation_sql": 'SELECT COUNT(*) FROM hr_attrition WHERE "MonthlyIncome" <= 0',
        "recommendation": "Investigate payroll data feed for missing/zero income entries.",
    },
    {
        "id": "LOAN-001", "table": "personal_loan", "dimension": "Uniqueness",
        "desc": "ID must be unique", "severity": "Critical",
        "violation_sql": """
            SELECT COALESCE(SUM(cnt),0) FROM (
                SELECT COUNT(*) as cnt FROM personal_loan
                GROUP BY "ID" HAVING COUNT(*) > 1
            ) sub
        """,
        "recommendation": "Block downstream use until key uniqueness is restored.",
    },
    {
        "id": "LOAN-002", "table": "personal_loan", "dimension": "Validity",
        "desc": "Experience must not be negative", "severity": "High",
        "violation_sql": 'SELECT COUNT(*) FROM personal_loan WHERE "Experience" < 0',
        "recommendation": "Correct or remove invalid negative experience values; likely a data entry error.",
    },
]


def get_row_count(conn, table):
    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
    return result.scalar()


def run_all_rules():
    findings = []
    with engine.connect() as conn:
        row_counts = {}
        for rule in RULES:
            table = rule["table"]
            if table not in row_counts:
                row_counts[table] = get_row_count(conn, table)
            total = int(row_counts[table])

            violations = int(conn.execute(text(rule["violation_sql"])).scalar())
            pass_rate = ((total - violations) / total * 100) if total > 0 else 0.0

            findings.append({
                **rule,
                "total": total,
                "violations": violations,
                "pass_rate": float(pass_rate),
            })
    return findings


def write_reports(findings):
    os.makedirs("reports/data-quality", exist_ok=True)

    # --- Detailed findings report ---
    lines = ["# SQL-Based Data Quality Findings Report", ""]
    lines.append("| Rule ID | Table | Dimension | Description | Severity | Violations | Total | Pass Rate | Recommendation |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for f in findings:
        lines.append(
            f"| {f['id']} | {f['table']} | {f['dimension']} | {f['desc']} | {f['severity']} "
            f"| {f['violations']} | {f['total']} | {f['pass_rate']:.2f}% "
            f"| {f['recommendation'] if f['violations'] > 0 else 'None needed'} |"
        )
    with open("reports/data-quality/sql-findings-report.md", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    # --- Dimension-level scorecard ---
    dimensions = {}
    for f in findings:
        dimensions.setdefault(f["dimension"], []).append(f["pass_rate"])

    score_lines = ["# Data Quality Scorecard by Dimension", ""]
    score_lines.append("| Dimension | Average Score |")
    score_lines.append("|---|---|")
    for dim, scores in dimensions.items():
        avg = sum(scores) / len(scores)
        score_lines.append(f"| {dim} | {avg:.2f}% |")

    overall = sum(f["pass_rate"] for f in findings) / len(findings)
    score_lines.append("")
    score_lines.append(f"**Overall Quality Score: {overall:.2f}%**")

    with open("reports/data-quality/sql-dimension-scorecard.md", "w", encoding="utf-8") as file:
        file.write("\n".join(score_lines))


if __name__ == "__main__":
    findings = run_all_rules()
    write_reports(findings)
    for f in findings:
        print(f"{f['id']} ({f['dimension']}): {f['violations']} violations / {f['total']} rows -> {f['pass_rate']:.2f}%")
    print("\nReports saved to reports/data-quality/")