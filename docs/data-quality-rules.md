# Data Quality Rules

Each rule includes exactly how it is measured, so documentation and code stay 
traceable to each other. Severity indicates business impact if the rule is 
violated: **Critical**, **High**, **Medium**, **Low**.

## bank.csv

| Rule ID | Column | Dimension | Pass Condition | Fail Condition | Measurement Method | Severity |
|---|---|---|---|---|---|---|
| BANK-001 | balance | Validity | balance >= 0 | balance < 0 | `SELECT COUNT(*) FROM bank WHERE balance < 0` | High |
| BANK-002 | age | Validity | age between 18–100 | age outside range | `SELECT COUNT(*) FROM bank WHERE age < 18 OR age > 100` | Medium |
| BANK-004 | job | Completeness | job is not null/blank | job is null or empty string | `SELECT COUNT(*) FROM bank WHERE job IS NULL OR TRIM(job) = ''` | Medium |
| BANK-005 | (all columns) | Uniqueness | row appears once | row appears 2+ times | `GROUP BY` all columns, `HAVING COUNT(*) > 1` | Medium |
| BANK-006 | deposit | Validity | value is 'yes' or 'no' | any other value | `SELECT COUNT(*) FROM bank WHERE deposit NOT IN ('yes','no')` | Low |

## Churn_Modelling.csv

| Rule ID | Column | Dimension | Pass Condition | Fail Condition | Measurement Method | Severity |
|---|---|---|---|---|---|---|
| CHURN-001 | CustomerId | Uniqueness | ID appears once | ID appears 2+ times | `GROUP BY "CustomerId" HAVING COUNT(*) > 1` | Critical |
| CHURN-002 | Balance | Validity | Balance >= 0 | Balance < 0 | `SELECT COUNT(*) FROM churn_modelling WHERE "Balance" < 0` | High |
| CHURN-003 | Age | Validity | Age between 18–100 | Age outside range | `SELECT COUNT(*) FROM churn_modelling WHERE "Age" < 18 OR "Age" > 100` | Medium |
| CHURN-005 | Geography | Completeness | Geography is not null/blank | Geography is null or empty | `SELECT COUNT(*) FROM churn_modelling WHERE "Geography" IS NULL OR TRIM("Geography") = ''` | Medium |
| CHURN-007 | Geography | Consistency | value is one of known set (France, Spain, Germany) | value outside known set | `SELECT COUNT(*) FROM churn_modelling WHERE "Geography" NOT IN ('France','Spain','Germany')` | Low |

## WA_Fn-UseC_-HR-Employee-Attrition.csv

| Rule ID | Column | Dimension | Pass Condition | Fail Condition | Measurement Method | Severity |
|---|---|---|---|---|---|---|
| HR-001 | EmployeeNumber | Uniqueness | ID appears once | ID appears 2+ times | `GROUP BY "EmployeeNumber" HAVING COUNT(*) > 1` | Critical |
| HR-002 | MonthlyIncome | Validity | MonthlyIncome > 0 | MonthlyIncome <= 0 | `SELECT COUNT(*) FROM hr_attrition WHERE "MonthlyIncome" <= 0` | High |
| HR-004 | Attrition | Completeness | Attrition is not null/blank | Attrition is null or empty | `SELECT COUNT(*) FROM hr_attrition WHERE "Attrition" IS NULL` | Medium |
| HR-007 | Attrition | Consistency | value is 'Yes' or 'No' | any other value | `SELECT COUNT(*) FROM hr_attrition WHERE "Attrition" NOT IN ('Yes','No')` | Low |

## Bank_Personal_Loan_Modelling.xlsx

| Rule ID | Column | Dimension | Pass Condition | Fail Condition | Measurement Method | Severity |
|---|---|---|---|---|---|---|
| LOAN-001 | ID | Uniqueness | ID appears once | ID appears 2+ times | `GROUP BY "ID" HAVING COUNT(*) > 1` | Critical |
| LOAN-002 | Experience | Validity | Experience >= 0 | Experience < 0 | `SELECT COUNT(*) FROM personal_loan WHERE "Experience" < 0` | High |
| LOAN-003 | Income | Completeness | Income is not null | Income is null | `SELECT COUNT(*) FROM personal_loan WHERE "Income" IS NULL` | High |
| LOAN-007 | Education | Consistency | value is 1, 2, or 3 | any other value | `SELECT COUNT(*) FROM personal_loan WHERE "Education" NOT IN (1,2,3)` | Low |

## How Scoring Works
For every rule: **Pass Rate = (Total Rows − Violations) / Total Rows × 100**

Dimension scores (Completeness %, Validity %, Uniqueness %, Consistency %) are 
the average pass rate of all rules tagged with that dimension, across all 
datasets. Overall Quality Score is the average pass rate across every rule, 
regardless of dimension.

## Cross-Dataset Rules

| Rule ID | Datasets Involved | Dimension | Condition | Severity |
|---|---|---|---|---|
| XREF-001 | bank.csv vs test.csv | Consistency | Same underlying schema should use consistent column names across exports (target column renamed `y` vs `deposit`) | Medium |

## Notes on Timeliness
All four datasets are static, one-time historical extracts with no live refresh 
pipeline in this project phase. Timeliness rules are not applicable here, but 
in a production system each dataset would have a "max age before considered 
stale" rule (e.g., "reject if last updated more than 24 hours ago").