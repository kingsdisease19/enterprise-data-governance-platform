"""
check_data_quality.py

Data Governance Platform - Data Quality Rule Checker
Runs a defined set of quality rules against a dataset and reports pass/fail
results, scored per rule and overall.

Usage:
    python scripts/check_data_quality.py
"""

import os
import pandas as pd


# ---------------------------------------------------------
# Reusable rule-check building blocks
# ---------------------------------------------------------

def rule_not_negative(df, column):
    violations = df[df[column] < 0]
    return len(violations), len(df)


def rule_between(df, column, min_val, max_val):
    violations = df[~df[column].between(min_val, max_val)]
    return len(violations), len(df)


def rule_unique(df, column):
    violations = df[df.duplicated(subset=[column], keep=False)]
    return len(violations), len(df)


def rule_no_duplicate_rows(df):
    violations = df[df.duplicated(keep=False)]
    return len(violations), len(df)


def rule_not_blank(df, column):
    violations = df[df[column].isna() | (df[column].astype(str).str.strip() == "")]
    return len(violations), len(df)


def rule_in_list(df, column, allowed_values):
    violations = df[~df[column].isin(allowed_values)]
    return len(violations), len(df)


# ---------------------------------------------------------
# Dataset definitions: rules translated from data-quality-rules.md
# ---------------------------------------------------------

def get_rules_for_dataset(name):
    """
    Each rule is a dict:
        id, description, severity, check (a function that returns (violations, total))
    """
    if name == "bank":
        return [
            {"id": "BANK-001", "desc": "balance should not be negative",
             "severity": "High", "check": lambda df: rule_not_negative(df, "balance")},
            {"id": "BANK-002", "desc": "age must be between 18 and 100",
             "severity": "Medium", "check": lambda df: rule_between(df, "age", 18, 100)},
            {"id": "BANK-004a", "desc": "job must not be blank",
             "severity": "Medium", "check": lambda df: rule_not_blank(df, "job")},
            {"id": "BANK-005", "desc": "no fully duplicate rows",
             "severity": "Medium", "check": lambda df: rule_no_duplicate_rows(df)},
            {"id": "BANK-006", "desc": "deposit must be yes or no",
             "severity": "Low", "check": lambda df: rule_in_list(df, "deposit", ["yes", "no"])},
        ]

    if name == "churn":
        return [
            {"id": "CHURN-001", "desc": "CustomerId must be unique",
             "severity": "Critical", "check": lambda df: rule_unique(df, "CustomerId")},
            {"id": "CHURN-002", "desc": "Balance must not be negative",
             "severity": "High", "check": lambda df: rule_not_negative(df, "Balance")},
            {"id": "CHURN-003", "desc": "Age must be between 18 and 100",
             "severity": "Medium", "check": lambda df: rule_between(df, "Age", 18, 100)},
            {"id": "CHURN-004", "desc": "EstimatedSalary must be greater than 0",
             "severity": "Medium", "check": lambda df: rule_between(df, "EstimatedSalary", 0.01, 10**9)},
            {"id": "CHURN-006", "desc": "no fully duplicate rows",
             "severity": "Medium", "check": lambda df: rule_no_duplicate_rows(df)},
        ]

    if name == "hr":
        return [
            {"id": "HR-001", "desc": "EmployeeNumber must be unique",
             "severity": "Critical", "check": lambda df: rule_unique(df, "EmployeeNumber")},
            {"id": "HR-002", "desc": "MonthlyIncome must be greater than 0",
             "severity": "High", "check": lambda df: rule_between(df, "MonthlyIncome", 1, 10**9)},
            {"id": "HR-003", "desc": "Age must be between 18 and 65",
             "severity": "Medium", "check": lambda df: rule_between(df, "Age", 18, 65)},
            {"id": "HR-004", "desc": "Attrition must be Yes or No",
             "severity": "Low", "check": lambda df: rule_in_list(df, "Attrition", ["Yes", "No"])},
            {"id": "HR-006", "desc": "PerformanceRating must be between 1 and 4",
             "severity": "Medium", "check": lambda df: rule_between(df, "PerformanceRating", 1, 4)},
        ]

    if name == "loan":
        return [
            {"id": "LOAN-001", "desc": "ID must be unique",
             "severity": "Critical", "check": lambda df: rule_unique(df, "ID")},
            {"id": "LOAN-002", "desc": "Experience must not be negative",
             "severity": "High", "check": lambda df: rule_not_negative(df, "Experience")},
            {"id": "LOAN-003", "desc": "Income must be greater than 0",
             "severity": "High", "check": lambda df: rule_between(df, "Income", 1, 10**9)},
            {"id": "LOAN-004", "desc": "CCAvg must not be negative",
             "severity": "Medium", "check": lambda df: rule_not_negative(df, "CCAvg")},
            {"id": "LOAN-005", "desc": "Age must be between 18 and 100",
             "severity": "Medium", "check": lambda df: rule_between(df, "Age", 18, 100)},
            {"id": "LOAN-006", "desc": "Education must be 1, 2, or 3",
             "severity": "Low", "check": lambda df: rule_in_list(df, "Education", [1, 2, 3])},
        ]

    return []


# ---------------------------------------------------------
# Core runner
# ---------------------------------------------------------

def run_quality_checks(df, dataset_key, display_name):
    rules = get_rules_for_dataset(dataset_key)
    results = []

    for rule in rules:
        violations, total = rule["check"](df)
        pass_rate = ((total - violations) / total * 100) if total > 0 else 0
        results.append({
            "id": rule["id"],
            "desc": rule["desc"],
            "severity": rule["severity"],
            "violations": violations,
            "total": total,
            "pass_rate": pass_rate,
        })

    return results


def write_report(display_name, results, output_path):
    lines = []
    lines.append(f"# Data Quality Report: {display_name}")
    lines.append("")
    lines.append("| Rule ID | Description | Severity | Violations | Total Rows | Pass Rate |")
    lines.append("|---|---|---|---|---|---|")

    for r in results:
        lines.append(
            f"| {r['id']} | {r['desc']} | {r['severity']} | {r['violations']} "
            f"| {r['total']} | {r['pass_rate']:.2f}% |"
        )

    overall_score = sum(r["pass_rate"] for r in results) / len(results) if results else 0
    lines.append("")
    lines.append(f"**Overall Quality Score: {overall_score:.2f}%**")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return overall_score


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    datasets = [
        {"key": "bank", "name": "bank.csv", "path": "datasets/raw/bank.csv", "sheet": None},
        {"key": "churn", "name": "Churn_Modelling.csv", "path": "datasets/raw/Churn_Modelling.csv", "sheet": None},
        {"key": "hr", "name": "HR Attrition", "path": "datasets/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv", "sheet": None},
        {"key": "loan", "name": "Personal Loan", "path": "datasets/raw/Bank_Personal_Loan_Modelling.xlsx", "sheet": "Data"},
    ]

    os.makedirs("reports/data-quality", exist_ok=True)

    scorecard_lines = ["# Data Quality Scorecard", "", "| Dataset | Overall Score |", "|---|---|"]

    for ds in datasets:
        if ds["path"].endswith(".xlsx"):
            df = pd.read_excel(ds["path"], sheet_name=ds["sheet"])
        else:
            df = pd.read_csv(ds["path"])

        results = run_quality_checks(df, ds["key"], ds["name"])
        output_path = f"reports/data-quality/{ds['key']}-quality-report.md"
        score = write_report(ds["name"], results, output_path)

        scorecard_lines.append(f"| {ds['name']} | {score:.2f}% |")
        print(f"{ds['name']}: {score:.2f}% -> {output_path}")

    with open("reports/data-quality/quality-scorecard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(scorecard_lines))

    print("Scorecard saved to reports/data-quality/quality-scorecard.md")