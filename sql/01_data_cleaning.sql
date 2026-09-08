-- ================================================================================
-- HR ANALYTICS: DATA CLEANING & PREPROCESSING PIPELINE
-- Database System: SQL Server / T-SQL (ANSI SQL Compatible structure)
-- Description: Cleans raw HR dataset, handles duplicates, formats categorical fields,
--              and creates calculated flag columns for downstream analytics.
-- ================================================================================

-- 1. Create Working Table Structure (if loading from raw csv staging)
IF OBJECT_ID('dbo.HR_Analytics', 'U') IS NOT NULL
    DROP TABLE dbo.HR_Analytics;

-- Note: Populate dbo.HR_Analytics with raw dataset (1470 rows) before running cleanup.

-- 2. Add Binary Attrition Flag for Aggregation Efficiency
ALTER TABLE dbo.HR_Analytics 
ADD Attrition_Value INT;

UPDATE dbo.HR_Analytics 
SET Attrition_Value = CASE 
    WHEN UPPER(RTRIM(LTRIM(Attrition))) = 'YES' THEN 1
    ELSE 0
END;

-- 3. Standardize Categorical Text Fields (Fix typos and inconsistent entries)
UPDATE dbo.HR_Analytics
SET BusinessTravel = 'Travel_Rarely'
WHERE BusinessTravel IN ('TravelRarely', 'Travel_Rarely', 'Rarely');

UPDATE dbo.HR_Analytics
SET Department = LTRIM(RTRIM(Department)),
    EducationField = LTRIM(RTRIM(EducationField)),
    JobRole = LTRIM(RTRIM(JobRole));

-- 4. Deduplication Logic (Remove redundant duplicate rows based on EmpID)
WITH RankedEmployees AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY EmpID) AS RowNum
    FROM dbo.HR_Analytics
)
DELETE FROM RankedEmployees
WHERE RowNum > 1;

-- 5. Drop Unnecessary/Blank Columns
IF EXISTS (
    SELECT 1 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'HR_Analytics' AND COLUMN_NAME = 'YearsWithCurrManager'
)
BEGIN
    ALTER TABLE dbo.HR_Analytics DROP COLUMN YearsWithCurrManager;
END;

-- 6. Verification & Data Quality Audit
SELECT 
    COUNT(*) AS Total_Records,
    SUM(Attrition_Value) AS Total_Attritions,
    ROUND(CAST(SUM(Attrition_Value) AS FLOAT) / COUNT(*) * 100, 2) AS Overall_Attrition_Rate_Pct
FROM dbo.HR_Analytics;

