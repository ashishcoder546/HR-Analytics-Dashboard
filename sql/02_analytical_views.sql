-- ================================================================================
-- HR ANALYTICS: ANALYTICAL VIEWS FOR POWER BI & REPORTING
-- Description: Creates modular SQL views for attrition analysis across demographics,
--              compensation, department, and tenure metrics.
-- ================================================================================

-- 1. Attrition by Age Group
DROP VIEW IF EXISTS dbo.vw_Attrition_By_Age;
GO
CREATE VIEW dbo.vw_Attrition_By_Age AS
SELECT 
    AgeGroup,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct
FROM dbo.HR_Analytics
GROUP BY AgeGroup;
GO

-- 2. Attrition by Department
DROP VIEW IF EXISTS dbo.vw_Attrition_By_Department;
GO
CREATE VIEW dbo.vw_Attrition_By_Department AS
SELECT 
    Department,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct,
    ROUND(AVG(CAST(MonthlyIncome AS FLOAT)), 2) AS Avg_Monthly_Income
FROM dbo.HR_Analytics
GROUP BY Department;
GO

-- 3. Attrition by Education Field
DROP VIEW IF EXISTS dbo.vw_Attrition_By_Education;
GO
CREATE VIEW dbo.vw_Attrition_By_Education AS
SELECT 
    EducationField,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct
FROM dbo.HR_Analytics
GROUP BY EducationField;
GO

-- 4. Attrition by Job Role
DROP VIEW IF EXISTS dbo.vw_Attrition_By_JobRole;
GO
CREATE VIEW dbo.vw_Attrition_By_JobRole AS
SELECT 
    JobRole,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct,
    ROUND(AVG(CAST(JobSatisfaction AS FLOAT)), 2) AS Avg_Satisfaction_Score
FROM dbo.HR_Analytics
GROUP BY JobRole;
GO

-- 5. Attrition by Salary Band / Slab
DROP VIEW IF EXISTS dbo.vw_Attrition_By_SalarySlab;
GO
CREATE VIEW dbo.vw_Attrition_By_SalarySlab AS
SELECT 
    SalarySlab,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct
FROM dbo.HR_Analytics
GROUP BY SalarySlab;
GO

-- 6. Attrition by Overtime Impact
DROP VIEW IF EXISTS dbo.vw_Attrition_By_Overtime;
GO
CREATE VIEW dbo.vw_Attrition_By_Overtime AS
SELECT 
    OverTime,
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Value) AS Attrition_Count,
    ROUND((CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*)) * 100, 2) AS Attrition_Rate_Pct
FROM dbo.HR_Analytics
GROUP BY OverTime;
GO

