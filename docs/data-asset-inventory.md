# Data Asset Inventory

| Asset | Description | Owner | Classification | Criticality | Source |
|---|---|---|---|---|---|
| Bank Customer Contact Register | Demographic + marketing contact data for term deposit campaigns | Data Owner (Marketing) | Confidential | Medium | bank.csv |
| Bank Account & Balance Records | Customer balance and loan/housing status | Data Owner (Finance) | Confidential | High | bank.csv |
| Retail Customer Register | Customer identity, geography, account tenure | Data Owner (Retail Banking) | Confidential | High | Churn_Modelling.csv |
| Customer Churn Status | Whether a customer exited the bank | Data Steward (Analytics) | Internal | Medium | Churn_Modelling.csv |
| Employee Records | Employee demographics, role, compensation | Data Owner (HR) | Restricted | High | WA_Fn-UseC_-HR-Employee-Attrition.csv |
| Employee Attrition & Performance Data | Attrition flag, satisfaction scores, performance ratings | Data Steward (HR Analytics) | Confidential | Medium | WA_Fn-UseC_-HR-Employee-Attrition.csv |

## Analyst Notes

- **Business problems supported:** targeted deposit marketing, customer churn 
  prevention, and employee retention planning.
- **Most critical fields:** `balance` and `deposit` (bank.csv), `CustomerId` and 
  `Exited` (Churn_Modelling.csv), `MonthlyIncome` and `Attrition` (HR dataset) — 
  these drive direct business decisions (who to contact, who to retain).
- **Sensitive fields:** `Surname`, `Geography`, `Balance`, `EstimatedSalary` 
  (customer PII/financial); `MonthlyIncome`, `PerformanceRating`, `Age` 
  (employee PII) — all require Confidential or Restricted classification.
- **Likely quality issues (once we inject them):** missing balances, duplicate 
  customer IDs, inconsistent job/education category spelling.
- **Impact if wrong:** marketing campaigns miss the right customers, retention 
  efforts target the wrong at-risk employees, and compliance risk increases if 
  PII is misclassified as lower-sensitivity than it actually is.

## Interview Notes
"A data asset inventory is a structured list of the organization's important 
data — what it is, who's accountable for it, how sensitive it is, and how 
critical it is to operations. It's the starting point of any governance 
program because you can't protect, improve, or assign ownership to data you 
haven't identified yet."