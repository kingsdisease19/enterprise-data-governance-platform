# Profiling Summary

## Biggest Risks
- `balance` in bank.csv contains negative values (-6,847 minimum) — needs 
  business rule clarification before any validation is enforced.
- `EmployeeCount` and `StandardHours` in the HR dataset are constants (always 
  1 and 80) — provide no analytical value and should be flagged, not treated 
  as meaningful fields.

## Best Quality Dataset
Churn_Modelling.csv — zero missing values, zero duplicates, CustomerId is a 
clean unique key, and all numeric ranges look business-plausible.

## Worst Quality Dataset (relatively)
bank.csv — while still zero missing/duplicates, it has ambiguous values 
(`pdays = -1`, negative balances) that need clarification before rules can be 
finalized.

## Interesting Findings
- HR Attrition dataset includes constant columns (`EmployeeCount`, 
  `StandardHours`, `Over18`) that add no value and should be documented as 
  such rather than removed silently.
- `pdays = -1` in bank.csv looks like an error at first glance but is actually 
  a documented placeholder — a good example of why profiling requires 
  understanding context, not just running statistics.

## Recommendations
- Confirm with a (fictional) business owner whether negative balances in 
  bank.csv are legitimate (e.g., overdraft) before writing a strict rule.
- Exclude constant columns from any future modeling or dashboard work.
- Carry the `-1` convention in `pdays` into the data dictionary so it isn't 
  misinterpreted later.
  
  ## Additional Finding (Bank_Personal_Loan_Modelling.xlsx)
`Experience` contains a minimum value of -3, which is invalid — you cannot 
have negative years of work experience. This is a clear data quality defect 
(not a documented placeholder like `pdays = -1` in bank.csv) and should be 
corrected or investigated in the `processed/` copy rather than the raw file.