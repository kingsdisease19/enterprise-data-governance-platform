# Data Dictionary

## bank.csv (Bank Marketing Dataset)

| Column | Meaning | Data Type | Required | Example |
|---|---|---|---|---|
| age | Customer's age in years | Integer | Yes | 42 |
| job | Customer's occupation category | Text | Yes | "management" |
| marital | Marital status | Text | Yes | "married" |
| education | Highest education level | Text | Yes | "secondary" |
| default | Whether customer has credit in default | Text (yes/no) | Yes | "no" |
| balance | Average yearly account balance in euros | Integer | Yes | 1350 |
| housing | Whether customer has a housing loan | Text (yes/no) | Yes | "yes" |
| loan | Whether customer has a personal loan | Text (yes/no) | Yes | "no" |
| contact | Method used to contact the customer | Text | Yes | "cellular" |
| day | Day of the month of last contact | Integer | Yes | 15 |
| month | Month of last contact | Text | Yes | "may" |
| duration | Duration of last contact, in seconds | Integer | Yes | 261 |
| campaign | Number of contacts made during this campaign | Integer | Yes | 2 |
| pdays | Days since last contact from a previous campaign (-1 = never contacted before) | Integer | Yes | -1 |
| previous | Number of contacts before this campaign | Integer | Yes | 0 |
| poutcome | Outcome of the previous marketing campaign | Text | Yes | "unknown" |
| deposit | Whether the customer subscribed to a term deposit (target field) | Text (yes/no) | Yes | "yes" |

## Churn_Modelling.csv (Retail Banking Customer Dataset)

| Column | Meaning | Data Type | Required | Example |
|---|---|---|---|---|
| RowNumber | Row position in the file (not a business field) | Integer | Yes | 1 |
| CustomerId | Unique identifier for each customer | Integer | Yes | 15634602 |
| Surname | Customer's last name | Text | Yes | "Hargrave" |
| CreditScore | Customer's credit score | Integer | Yes | 619 |
| Geography | Customer's country | Text | Yes | "France" |
| Gender | Customer's gender | Text | Yes | "Female" |
| Age | Customer's age in years | Integer | Yes | 42 |
| Tenure | Number of years as a customer | Integer | Yes | 2 |
| Balance | Current account balance | Decimal | Yes | 83807.86 |
| NumOfProducts | Number of bank products the customer uses | Integer | Yes | 1 |
| HasCrCard | Whether the customer has a credit card (1=yes, 0=no) | Integer (flag) | Yes | 1 |
| IsActiveMember | Whether the customer is actively using services (1=yes, 0=no) | Integer (flag) | Yes | 1 |
| EstimatedSalary | Estimated annual salary | Decimal | Yes | 101348.88 |
| Exited | Whether the customer left the bank (1=yes, 0=no) — target field | Integer (flag) | Yes | 1 |

## WA_Fn-UseC_-HR-Employee-Attrition.csv (HR Dataset)

| Column | Meaning | Data Type | Required | Example |
|---|---|---|---|---|
| Age | Employee's age in years | Integer | Yes | 41 |
| Attrition | Whether the employee left the company (target field) | Text (Yes/No) | Yes | "Yes" |
| BusinessTravel | How frequently the employee travels for work | Text | Yes | "Travel_Rarely" |
| DailyRate | Employee's daily pay rate | Integer | Yes | 1102 |
| Department | Department the employee works in | Text | Yes | "Sales" |
| DistanceFromHome | Distance from home to work, in miles | Integer | Yes | 1 |
| Education | Education level, coded 1–5 | Integer (code) | Yes | 2 |
| EducationField | Field of study | Text | Yes | "Life Sciences" |
| EmployeeCount | Constant value, always 1 (not analytically useful) | Integer | Yes | 1 |
| EmployeeNumber | Unique identifier for each employee | Integer | Yes | 1 |
| EnvironmentSatisfaction | Satisfaction with work environment, coded 1–4 | Integer (code) | Yes | 2 |
| Gender | Employee's gender | Text | Yes | "Female" |
| HourlyRate | Employee's hourly pay rate | Integer | Yes | 94 |
| JobInvolvement | Level of job involvement, coded 1–4 | Integer (code) | Yes | 3 |
| JobLevel | Seniority level, coded 1–5 | Integer (code) | Yes | 2 |
| JobRole | Employee's job title | Text | Yes | "Sales Executive" |
| JobSatisfaction | Job satisfaction, coded 1–4 | Integer (code) | Yes | 4 |
| MaritalStatus | Marital status | Text | Yes | "Single" |
| MonthlyIncome | Employee's monthly salary | Integer | Yes | 5993 |
| MonthlyRate | Monthly rate (distinct from income; source-defined) | Integer | Yes | 19479 |
| NumCompaniesWorked | Number of companies worked at previously | Integer | Yes | 8 |
| Over18 | Whether employee is over 18 (constant, always "Y") | Text | Yes | "Y" |
| OverTime | Whether the employee works overtime | Text (Yes/No) | Yes | "Yes" |
| PercentSalaryHike | Percentage salary increase in last review | Integer | Yes | 11 |
| PerformanceRating | Performance rating, coded 1–4 | Integer (code) | Yes | 3 |
| RelationshipSatisfaction | Satisfaction with workplace relationships, coded 1–4 | Integer (code) | Yes | 1 |
| StandardHours | Standard working hours (constant, always 80) | Integer | Yes | 80 |
| StockOptionLevel | Level of stock options granted, coded 0–3 | Integer (code) | Yes | 0 |
| TotalWorkingYears | Total years of work experience | Integer | Yes | 8 |
| TrainingTimesLastYear | Number of trainings attended last year | Integer | Yes | 0 |
| WorkLifeBalance | Work-life balance rating, coded 1–4 | Integer (code) | Yes | 1 |
| YearsAtCompany | Years at the current company | Integer | Yes | 6 |
| YearsInCurrentRole | Years in current role | Integer | Yes | 4 |
| YearsSinceLastPromotion | Years since last promotion | Integer | Yes | 0 |
| YearsWithCurrManager | Years with current manager | Integer | Yes | 5 |

## Bank_Personal_Loan_Modelling.xlsx (Personal Loan Dataset)

| Column | Meaning | Data Type | Required | Example |
|---|---|---|---|---|
| ID | Unique identifier for each customer | Integer | Yes | 1 |
| Age | Customer's age in years | Integer | Yes | 45 |
| Experience | Years of professional work experience | Integer | Yes | 20 |
| Income | Annual income, in thousands of dollars | Integer | Yes | 75 |
| ZIP Code | Customer's home ZIP code | Integer | Yes | 94720 |
| Family | Number of family members | Integer | Yes | 3 |
| CCAvg | Average monthly credit card spending, in thousands of dollars | Decimal | Yes | 1.5 |
| Education | Education level (1=Undergrad, 2=Graduate, 3=Advanced/Professional) | Integer (code) | Yes | 2 |
| Mortgage | Value of house mortgage, in thousands of dollars (0 = no mortgage) | Integer | Yes | 0 |
| Personal Loan | Whether customer accepted a personal loan offer (target field) | Integer (flag) | Yes | 0 |
| Securities Account | Whether customer has a securities account | Integer (flag) | Yes | 0 |
| CD Account | Whether customer has a certificate of deposit account | Integer (flag) | Yes | 0 |
| Online | Whether customer uses online banking | Integer (flag) | Yes | 1 |
| CreditCard | Whether customer holds a credit card from this bank | Integer (flag) | Yes | 0 |