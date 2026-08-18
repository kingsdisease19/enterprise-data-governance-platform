## Executive Summary

15 data quality rules were evaluated across 4 datasets (27,632 total rows), 
covering all four core dimensions: Completeness, Validity, Uniqueness, and 
Consistency.

**13 of 15 rules passed at 100%.** Two failures were identified, both in the 
Validity dimension, both High severity:

1. **BANK-001** — 688 rows (6.16%) in `bank.csv` contain a negative `balance`. 
   Recommendation: confirm with the business whether overdrafts are a valid 
   state; if not, this indicates a source system defect requiring investigation.

2. **LOAN-002** — 52 rows (1.04%) in `personal_loan` contain a negative 
   `Experience` value. Recommendation: correct or remove these records; 
   negative work experience is not logically possible and is very likely a 
   data entry error rather than a valid business state.

No Completeness, Uniqueness, or Consistency violations were found in any 
dataset. All primary keys (`CustomerId`, `EmployeeNumber`, `ID`) are fully 
unique, and no missing values were detected in any checked field.

**Overall recommendation:** Both findings should be routed to their respective 
data owners (Finance for BANK-001, Lending for LOAN-002) for root-cause 
investigation before these datasets are used in any downstream reporting or 
modeling.

---