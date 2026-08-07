# Data Quality Rules

Each rule below is written so it can be directly translated into a check a 
script can run automatically. Severity indicates business impact if the rule 
is violated: **Critical** (blocks trustworthy decision-making), **High** 
(significant but not blocking), **Medium** (worth monitoring), **Low** (minor).

## bank.csv

| Rule ID | Column | Dimension | Condition | Severity |
|---|---|---|---|---|
| BANK-001 | balance | Accuracy | Should not be negative (flag for business review, not auto-reject) | High |
| BANK-002 | age | Validity | Must be between 18 and 100 | Medium |
| BANK-003 | pdays | Validity | Must be -1 (placeholder) or a positive integer | Low |
| BANK-004 | job, marital, education | Completeness | Must not be blank | Medium |
| BANK-005 | (all rows) | Uniqueness | No fully duplicate rows | Medium |
| BANK-006 | deposit | Validity | Must be exactly "yes" or "no" | Low |

## Churn_Modelling.csv

| Rule ID | Column | Dimension | Condition | Severity |
|---|---|---|---|---|
| CHURN-001 | CustomerId | Uniqueness | Must be unique across all rows | Critical |
| CHURN-002 | Balance | Validity | Must not be negative | High |
| CHURN-003 | Age | Validity | Must be between 18 and 100 | Medium |
| CHURN-004 | EstimatedSalary | Validity | Must be greater than 0 | Medium |
| CHURN-005 | Geography | Consistency | Must be one of a known, fixed list of countries | Low |
| CHURN-006 | (all rows) | Uniqueness | No fully duplicate rows | Medium |

## WA_Fn-UseC_-HR-Employee-Attrition.csv

| Rule ID | Column | Dimension | Condition | Severity |
|---|---|---|---|---|
| HR-001 | EmployeeNumber | Uniqueness | Must be unique across all rows | Critical |
| HR-002 | MonthlyIncome | Validity | Must be greater than 0 | High |
| HR-003 | Age | Validity | Must be between 18 and 65 | Medium |
| HR-004 | Attrition | Validity | Must be exactly "Yes" or "No" | Low |
| HR-005 | EmployeeCount | Consistency | Must always equal 1 (documented constant, not an error) | Low |
| HR-006 | PerformanceRating | Validity | Must be between 1 and 4 | Medium |

## Bank_Personal_Loan_Modelling.xlsx

| Rule ID | Column | Dimension | Condition | Severity |
|---|---|---|---|---|
| LOAN-001 | ID | Uniqueness | Must be unique across all rows | Critical |
| LOAN-002 | Experience | Validity | Must not be negative | High |
| LOAN-003 | Income | Validity | Must be greater than 0 | High |
| LOAN-004 | CCAvg | Validity | Must not be negative | Medium |
| LOAN-005 | Age | Validity | Must be between 18 and 100 | Medium |
| LOAN-006 | Education | Validity | Must be 1, 2, or 3 (per coded scale) | Low |

## Cross-Dataset Rules

| Rule ID | Datasets Involved | Dimension | Condition | Severity |
|---|---|---|---|---|
| XREF-001 | bank.csv vs test.csv | Consistency | Same underlying schema should use consistent column names across exports (target column renamed `y` vs `deposit`) | Medium |

## Notes on Timeliness
All four datasets are static, one-time historical extracts with no live refresh 
pipeline in this project phase. Timeliness rules are not applicable here, but 
in a production system each dataset would have a "max age before considered 
stale" rule (e.g., "reject if last updated more than 24 hours ago").