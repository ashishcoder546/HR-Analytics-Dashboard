# HR Analytics & Attrition Project - Interview Talking Points & FAQ Guide

Use this guide to confidently explain this project in interviews for **Data Analyst**, **BI Engineer**, or **Data Engineer** positions.

---

## 🎤 1. 60-Second Elevator Pitch (Opening Statement)

> "In this project, I built an end-to-end workforce intelligence system analyzing **1,470 employee records** to identify the root causes of employee turnover and help HR leaders reduce costly attrition. 
> 
> I engineered a **Python ETL pipeline** for automated data validation, built modular **T-SQL data cleaning scripts and analytical views**, developed an interactive **Power BI dashboard**, and trained a **Random Forest Machine Learning model** to predict employee departure risk. 
> 
> A key business insight I discovered was that employees working regular overtime experienced a **30.5% attrition rate**—nearly **3 times higher** than non-overtime staff (10.4%). Based on this, I delivered actionable recommendations for workload caps and targeted retention strategies."

---

## 🎯 2. STAR Method Project Breakdown

### **Situation (Context):**
Employee turnover causes significant costs in recruitment, onboarding, and productivity loss. HR leaders lacked visibility into why employees were leaving and which departments were most vulnerable.

### **Task (Your Objective):**
Clean raw HR data, aggregate key workforce metrics using SQL, build dynamic visual dashboards in Power BI, and create a predictive risk model to alert HR before employees resign.

### **Action (What You Did):**
- **Data Engineering & SQL:** Created CTEs (`ROW_NUMBER`) to handle duplicate rows, built 6 modular SQL views (`vw_Attrition_By_Age`, `vw_Attrition_By_Department`), and applied `NTILE(4)` window functions to analyze income quartiles.
- **Python Data Pipeline & Machine Learning:** Wrote an automated Python pipeline (`scripts/hr_analytics_pipeline.py`) to process raw CSVs and trained a **Random Forest Classifier** (`scripts/train_attrition_model.py`) to rank top predictive factors of turnover.
- **Power BI & DAX:** Formulated explicit DAX measures (`CALCULATE`, `DIVIDE`) to construct interactive KPI cards and demographic matrix slicers.

### **Result (Business Impact):**
- Identified that **Overtime Work (30.5%)** and **Sales Department (20.6%)** had the highest churn risk.
- Developed a 4-factor retention risk score that identified **60 high-risk employees** with an observed turnover rate of **31.9%**.

---

## ❓ 3. Top Interview Questions & Technical Answers

### Q1: *"How did you handle dirty or duplicate data in SQL?"*
**Answer:**  
"I used SQL Window Functions—specifically `ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY EmpID)` inside a Common Table Expression (CTE)—to isolate and delete duplicate records cleanly. I also standardized categorical columns like `BusinessTravel` and added binary flag columns (`Attrition_Value = 1/0`) to simplify aggregation performance."

### Q2: *"Why did you use DAX instead of pre-aggregating everything in SQL?"*
**Answer:**  
"While SQL views handle base-level aggregations efficiently, DAX allows dynamic filter contexts in Power BI. For example, when a user selects a specific department or age group slicer, DAX measures like `CALCULATE([Attrition Rate %], 'HR Data'[Over Time] = "Yes")` dynamically recalculate without requiring hardcoded static tables."

### Q3: *"How does your Machine Learning model predict attrition?"*
**Answer:**  
"I built a Random Forest Classifier in Python (`scikit-learn`) using features like Monthly Income, Overtime, Age, Job Satisfaction, and Years at Company. I evaluated performance using ROC-AUC score and extracted feature importances, confirming that Monthly Income, Overtime, and Distance From Home were the strongest predictors of turnover."
