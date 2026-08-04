#!/usr/bin/env python
"""
Data Governance Platform - Data Profiling Script

Loads a CSV, profiles it, and saves a summary report.

Usage:
    python scripts/profile_dataset.py datasets/raw/bank.csv
"""

import sys
import os
import pandas as pd
from pathlib import Path


def profile_dataset(csv_path):
    """
    Profile a CSV dataset and generate a summary report.
    
    Args:
        csv_path (str): Path to the CSV file to profile
        
    Returns:
        dict: Dictionary containing profile summary
    """
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        return None
    
    # Load the dataset
    df = pd.read_csv(csv_path)
    
    # Generate profile summary
    profile = {
        "file": csv_path,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
    }
    
    return profile, df


def save_report(profile, df, output_path):
    """
    Save the profile summary to a report file.
    
    Args:
        profile (dict): Profile summary dictionary
        df (pd.DataFrame): The profiled dataframe
        output_path (str): Path to save the report
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("DATA PROFILING REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"File: {profile['file']}\n")
        f.write(f"Rows: {profile['rows']}\n")
        f.write(f"Columns: {profile['columns']}\n")
        f.write(f"Memory Usage: {profile['memory_usage']:.2f} MB\n")
        f.write(f"Duplicate Rows: {profile['duplicates']}\n\n")
        
        f.write("COLUMN INFORMATION\n")
        f.write("-" * 60 + "\n")
        for col in profile['column_names']:
            f.write(f"\n{col}:\n")
            f.write(f"  Data Type: {profile['data_types'][col]}\n")
            f.write(f"  Missing Values: {profile['missing_values'][col]}\n")
            if df[col].dtype in ['int64', 'float64']:
                f.write(f"  Min: {df[col].min()}\n")
                f.write(f"  Max: {df[col].max()}\n")
                f.write(f"  Mean: {df[col].mean():.2f}\n")
    
    print(f"Report saved to: {output_path}")


def main():
    """Main entry point for the profiling script."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/profile_dataset.py <csv_path>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    # Profile the dataset
    result = profile_dataset(csv_path)
    if result is None:
        sys.exit(1)
    
    profile, df = result
    
    # Generate output path
    filename = Path(csv_path).stem
    output_path = f"reports/profiles/{filename}_profile.txt"
    
    # Save the report
    save_report(profile, df, output_path)
    
    print(f"\nProfiling completed for: {csv_path}")
    print(f"Rows: {profile['rows']}, Columns: {profile['columns']}")


if __name__ == "__main__":
    main()
