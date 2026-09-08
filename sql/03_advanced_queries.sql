-- ================================================================================
-- HR ANALYTICS: ADVANCED BUSINESS QUERY BENCHMARKS & RISK METRICS
-- Description: Advanced T-SQL queries utilizing CTEs, Window Functions (NTILE, DENSE_RANK),
--              and composite risk modeling for workforce retention insights.
-- ================================================================================

-- Query 1: High-Risk Employee Profiling (Overtime + Low Satisfaction + Low Pay)
WITH RiskProfile AS (
    SELECT 
        EmpID,
        Department,
        JobRole,
        Age,
        MonthlyIncome,
        OverTime,
        JobSatisfaction,
        WorkLifeBalance,
        Attrition_Value,
        CASE 
            WHEN OverTime = 'Yes' AND JobSatisfaction <= 2 AND WorkLifeBalance <= 2 THEN 'High Risk'
            WHEN OverTime = 'Yes' OR JobSatisfaction <= 2 OR WorkLifeBalance <= 2 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS Retention_Risk_Category
    FROM dbo.HR_Analytics
)
SELECT 
    Retention_Risk_Category,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Actual_Attritions,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Historical_Attrition_Rate_Pct
FROM RiskProfile
GROUP BY Retention_Risk_Category
ORDER BY Historical_Attrition_Rate_Pct DESC;


-- Query 2: Salary Quartile Attrition Ranking using NTILE()
WITH IncomeQuartiles AS (
    SELECT 
        EmpID,
        Department,
        JobRole,
        MonthlyIncome,
        Attrition_Value,
        NTILE(4) OVER (ORDER BY MonthlyIncome ASC) AS Income_Quartile
    FROM dbo.HR_Analytics
)
SELECT 
    Income_Quartile,
    MIN(MonthlyIncome) AS Min_Income,
    MAX(MonthlyIncome) AS Max_Income,
    COUNT(*) AS Employee_Count,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct
FROM IncomeQuartiles
GROUP BY Income_Quartile
ORDER BY Income_Quartile ASC;


-- Query 3: Role-wise Attrition vs. Department Average Compensation Benchmark
WITH DepartmentMetrics AS (
    SELECT 
        Department,
        AVG(CAST(MonthlyIncome AS FLOAT)) AS Dept_Avg_Income
    FROM dbo.HR_Analytics
    GROUP BY Department
),
RoleMetrics AS (
    SELECT 
        JobRole,
        Department,
        COUNT(*) AS Total_Employees,
        SUM(Attrition_Value) AS Attritions,
        AVG(CAST(MonthlyIncome AS FLOAT)) AS Role_Avg_Income
    FROM dbo.HR_Analytics
    GROUP BY JobRole, Department
)
SELECT 
    r.Department,
    r.JobRole,
    r.Total_Employees,
    r.Attritions,
    ROUND((CAST(r.Attritions AS FLOAT) / r.Total_Employees) * 100, 2) AS Attrition_Rate_Pct,
    ROUND(r.Role_Avg_Income, 2) AS Role_Avg_Income,
    ROUND(d.Dept_Avg_Income, 2) AS Dept_Avg_Income,
    ROUND(r.Role_Avg_Income - d.Dept_Avg_Income, 2) AS Compensation_Variance
FROM RoleMetrics r
JOIN DepartmentMetrics d ON r.Department = d.Department
ORDER BY Attrition_Rate_Pct DESC;

