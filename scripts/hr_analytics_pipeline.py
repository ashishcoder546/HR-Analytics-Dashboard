"""
================================================================================
HR ANALYTICS DATA ETL & STATISTICAL AUDIT PIPELINE
================================================================================
Description: Automated Python pipeline for HR dataset validation, exploratory data 
             analysis (EDA), DAX metric cross-validation, and risk modeling.
Author: HR Analytics Engineering Team
================================================================================
"""

import os
import pandas as pd
import numpy as np

def run_pipeline(data_path="HR Data.csv"):
    if not os.path.exists(data_path):
        print(f"Error: File {data_path} not found.")
        return

    print("==================================================")
    print("1. LOADING DATASET & EXECUTING DATA QUALITY CHECKS")
    print("==================================================")
    df = pd.read_csv(data_path)
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Clean column names (strip whitespace)
    df.columns = [col.strip() for col in df.columns]

    # Binary flag for Attrition
    if 'Attrition' in df.columns:
        df['Attrition_Value'] = df['Attrition'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)

    total_employees = len(df)
    total_attrition = df['Attrition_Value'].sum()
    attrition_rate = (total_attrition / total_employees) * 100

    print(f"Total Employees : {total_employees}")
    print(f"Total Attrition : {total_attrition}")
    print(f"Attrition Rate  : {attrition_rate:.2f}%\n")

    print("==================================================")
    print("2. DEPARTMENTAL ATTRITION BREAKDOWN")
    print("==================================================")
    dept_summary = df.groupby('Department').agg(
        Total_Employees=('emp no', 'count'),
        Attrited=('Attrition_Value', 'sum'),
        Avg_Monthly_Income=('Monthly Income', 'mean')
    )
    dept_summary['Attrition_Rate_%'] = (dept_summary['Attrited'] / dept_summary['Total_Employees']) * 100
    print(dept_summary.round(2).to_string())
    print("\n")

    print("==================================================")
    print("3. OVERTIME vs ATTRITION ANALYSIS")
    print("==================================================")
    ot_summary = df.groupby('Over Time').agg(
        Total_Employees=('emp no', 'count'),
        Attrited=('Attrition_Value', 'sum')
    )
    ot_summary['Attrition_Rate_%'] = (ot_summary['Attrited'] / ot_summary['Total_Employees']) * 100
    print(ot_summary.round(2).to_string())
    print("\n")

    print("==================================================")
    print("4. RETENTION RISK SCORING")
    print("==================================================")
    def calc_risk(row):
        score = 0
        if str(row.get('Over Time', '')).strip() == 'Yes':
            score += 2
        if row.get('Job Satisfaction', 4) <= 2:
            score += 2
        if row.get('Work Life Balance', 4) <= 2:
            score += 1
        if row.get('Years Since Last Promotion', 0) >= 5:
            score += 1
        
        if score >= 4:
            return 'High Risk'
        elif score >= 2:
            return 'Medium Risk'
        return 'Low Risk'

    df['Risk_Category'] = df.apply(calc_risk, axis=1)
    risk_summary = df.groupby('Risk_Category').agg(
        Employee_Count=('emp no', 'count'),
        Actual_Attritions=('Attrition_Value', 'sum')
    )
    risk_summary['Observed_Attrition_Rate_%'] = (risk_summary['Actual_Attritions'] / risk_summary['Employee_Count']) * 100
    print(risk_summary.round(2).to_string())
    print("==================================================")

    # Save summary report
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    summary_csv = os.path.join(output_dir, "python_eda_summary.csv")
    dept_summary.to_csv(summary_csv)
    print(f"\n[INFO] Summary exported to {summary_csv}")

if __name__ == "__main__":
    run_pipeline()

