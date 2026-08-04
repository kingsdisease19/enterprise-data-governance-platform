#!/usr/bin/env python
"""
Data Governance Platform - Data Profiling Script

Loads a CSV or Excel file, profiles it, and saves a summary report.

Usage:
    python scripts/profile_dataset.py datasets/raw/bank.csv
    python scripts/profile_dataset.py datasets/raw/bank.xlsx 0
"""

import os
import sys
from pathlib import Path

import pandas as pd


def profile_dataset(filepath, sheet_name=0):
    """
    Profile a CSV or Excel dataset and generate a summary report.

    Args:
        filepath (str): Path to the CSV or Excel file to profile
        sheet_name (int | str, optional): Excel sheet name or index. Defaults to 0.

    Returns:
        tuple: (profile dict, DataFrame)
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None

    filename = os.path.basename(filepath)

    if str(filepath).lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(filepath, sheet_name=sheet_name)
    else:
        df = pd.read_csv(filepath)

    profile = {
        "file": filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
    }

    return profile, df


def format_profile_report(profile, df):
    """Format the profiling results as Markdown."""
    lines = []
    lines.append("# Data Profiling Report")
    lines.append("")
    lines.append(f"- File: {profile['file']}")
    lines.append(f"- Rows: {profile['rows']}")
    lines.append(f"- Columns: {profile['columns']}")
    lines.append(f"- Memory Usage: {profile['memory_usage']:.2f} MB")
    lines.append(f"- Duplicate Rows: {profile['duplicates']}")
    lines.append("")
    lines.append("## Column Information")
    lines.append("")

    for col in profile["column_names"]:
        lines.append(f"### {col}")
        lines.append(f"- Data Type: {profile['data_types'][col]}")
        lines.append(f"- Missing Values: {profile['missing_values'][col]}")
        if pd.api.types.is_numeric_dtype(df[col]):
            lines.append(f"- Min: {df[col].min()}")
            lines.append(f"- Max: {df[col].max()}")
            lines.append(f"- Mean: {df[col].mean():.2f}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    """Main entry point for the profiling script."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/profile_dataset.py <path-to-file> [sheet_name]")
        sys.exit(1)

    input_path = sys.argv[1]
    sheet = sys.argv[2] if len(sys.argv) > 2 else 0

    result = profile_dataset(input_path, sheet_name=sheet)
    if result is None:
        sys.exit(1)

    profile, df = result
    report = format_profile_report(profile, df)

    output_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = Path("reports/data-profiling") / f"{output_name}-profile.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(report, encoding="utf-8")

    print(f"Profile saved to {output_path}")
    print()
    print(report)


if __name__ == "__main__":
    main()
