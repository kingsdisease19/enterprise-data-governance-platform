# Business Rules

| Field | Dataset | Rule | Reason |
|---|---|---|---|
| balance | bank.csv | Should not be negative (proposed) | Found min of -6,847 during profiling — needs business confirmation on whether overdrafts are valid or a data error |
| pdays | bank.csv | -1 is a valid placeholder meaning "never previously contacted" | Confirmed via profiling; not a data quality error, must be documented so future analysts don't flag it incorrectly |
| CustomerId | Churn_Modelling.csv | Must be unique | Verified 0 duplicates; this is the natural primary key |
| Age | Churn_Modelling.csv, HR Attrition | Should be between 18 and 100 (proposed) | Verified actual range is 18–92 (Churn) and 18–60 (HR) — both within reasonable bounds |
| MonthlyIncome | HR Attrition | Must be greater than 0 | Verified min is 1,009 — no zero or negative values found |
| EmployeeCount | HR Attrition | Should always equal 1 | Verified min=max=1 — column appears to be a constant, worth flagging as low-value/redundant during modeling |