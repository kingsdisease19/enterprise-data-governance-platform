# SQL-Based Data Quality Findings Report

| Rule ID | Table | Dimension | Description | Severity | Violations | Total | Pass Rate | Recommendation |
|---|---|---|---|---|---|---|---|---|
| BANK-001 | bank | Validity | balance should not be negative | High | 688 | 11162 | 93.84% | Confirm with business whether overdrafts are valid; if not, investigate source system. |
| BANK-005 | bank | Uniqueness | no fully duplicate rows | Medium | 0 | 11162 | 100.00% | None needed |
| CHURN-001 | churn_modelling | Uniqueness | CustomerId must be unique | Critical | 0 | 10000 | 100.00% | None needed |
| CHURN-002 | churn_modelling | Validity | Balance must not be negative | High | 0 | 10000 | 100.00% | None needed |
| HR-001 | hr_attrition | Uniqueness | EmployeeNumber must be unique | Critical | 0 | 1470 | 100.00% | None needed |
| HR-002 | hr_attrition | Validity | MonthlyIncome must be greater than 0 | High | 0 | 1470 | 100.00% | None needed |
| LOAN-001 | personal_loan | Uniqueness | ID must be unique | Critical | 0 | 5000 | 100.00% | None needed |
| LOAN-002 | personal_loan | Validity | Experience must not be negative | High | 52 | 5000 | 98.96% | Correct or remove invalid negative experience values; likely a data entry error. |