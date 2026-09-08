# Power BI DAX Measures & Metrics Documentation

This document serves as the technical documentation for all Data Analysis Expressions (DAX) measures implemented in the **HR Analytics Dashboard** (`HR_Analytics_Dashboard_.pbix`).

---

## Key Performance Indicators (KPIs)

### 1. Total Employees
Calculates the distinct count of employees across the organization.
```dax
Total Employees = COUNT('HR Data'[emp no])
```

### 2. Total Attrition Count
Counts the total number of employees who have left the organization (`Attrition = "Yes"`).
```dax
Attrition Count = 
CALCULATE(
    COUNT('HR Data'[emp no]),
    'HR Data'[Attrition] = "Yes"
)
```

### 3. Attrition Rate (%)
Calculates the overall organizational turnover percentage.
```dax
Attrition Rate % = 
DIVIDE(
    [Attrition Count],
    [Total Employees],
    0
) * 100
```

### 4. Active Employees Count
Calculates current active headcount.
```dax
Active Employees = [Total Employees] - [Attrition Count]
```

### 5. Average Monthly Income
Calculates the baseline average monthly compensation.
```dax
Avg Monthly Income = AVERAGE('HR Data'[Monthly Income])
```

### 6. Average Age
Calculates average workforce age.
```dax
Avg Age = AVERAGE('HR Data'[Age])
```

---

## Departmental & Overtime Metrics

### 7. Overtime Attrition Rate (%)
Calculates attrition percentage specifically for employees working overtime.
```dax
Overtime Attrition Rate % = 
CALCULATE(
    [Attrition Rate %],
    'HR Data'[Over Time] = "Yes"
)
```

### 8. Attrition Impact by Job Satisfaction
Calculates attrition count for low job satisfaction scores (1 or 2 out of 4).
```dax
Low Satisfaction Attrition = 
CALCULATE(
    [Attrition Count],
    'HR Data'[Job Satisfaction] <= 2
)
```

