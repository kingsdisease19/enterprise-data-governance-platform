-- SELECT examples
-- Pulling specific columns/rows
SELECT "Age", "Income", "Experience" FROM personal_loan LIMIT 10;

SELECT "Age", "Income" FROM personal_loan WHERE "Income" > 100 TOP 10;


-- GROUP BY / HAVING examples
-- Aggregating data into buckets
SELECT "Education", AVG("Income") AS avg_income, COUNT(*) AS num_customers
FROM personal_loan
GROUP BY "Education";

SELECT "Education", AVG("Income") AS avg_income, COUNT(*) AS num_customers
FROM personal_loan
GROUP BY "Education"
HAVING COUNT(*) > 1000;

SELECT job, AVG(balance) AS avg_balance, COUNT(*) AS num_customers
FROM bank
GROUP BY job
ORDER BY avg_balance DESC;


-- NULL checks
-- Verifying data completeness
SELECT * FROM churn_modelling WHERE "Balance" IS NULL;

SELECT * FROM personal_loan WHERE "Age" IS NULL;

SELECT * FROM bank WHERE balance IS NULL;


-- Duplicate detection
-- Finding repeated key values
SELECT "CustomerId", COUNT(*) AS times_seen
FROM churn_modelling
GROUP BY "CustomerId"
HAVING COUNT(*) > 1;

SELECT "ID", COUNT(*) AS times_seen
FROM personal_loan
GROUP BY "ID"
HAVING COUNT(*) > 1;


-- Business-rule validation as raw SQL
-- Testing data quality rules
SELECT "ID", "Age", "Experience" FROM personal_loan WHERE "Experience" < 0;

SELECT COUNT(*) AS negative_balance_count FROM bank WHERE balance < 0;

SELECT * FROM personal_loan WHERE "Age" < 18 OR "Age" > 100;


-- JOIN examples
-- Creating a reference/lookup table for education labels
CREATE TABLE education_labels (
    code INTEGER,
    label TEXT
);

INSERT INTO education_labels (code, label) VALUES
(1, 'Undergraduate'),
(2, 'Graduate'),
(3, 'Advanced/Professional');

-- Joining personal_loan with reference table to display readable labels
SELECT p."ID", p."Income", e.label AS education_level
FROM personal_loan p
JOIN education_labels e ON p."Education" = e.code;
