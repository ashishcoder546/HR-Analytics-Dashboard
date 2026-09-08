"""
================================================================================
PREDICTIVE HR ATTRITION MODEL (MACHINE LEARNING PIPELINE)
================================================================================
Description: Trains a Random Forest Classifier to predict employee turnover risk,
             evaluates performance metrics (ROC-AUC, Precision, Recall), and 
             extracts key feature importances.
Author: HR Analytics Engineering Team
================================================================================
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def train_model(data_path="HR Data.csv"):
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    print("==================================================")
    print("1. LOADING & PREPROCESSING DATASET FOR ML")
    print("==================================================")
    df = pd.read_csv(data_path)
    df.columns = [c.strip() for c in df.columns]

    # Target variable
    df['Target'] = df['Attrition'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)

    # Key features selection
    features = [
        'Age', 'Daily Rate', 'Distance From Home', 'Education', 'Environment Satisfaction',
        'Hourly Rate', 'Job Involvement', 'Job Level', 'Job Satisfaction', 'Monthly Income',
        'Monthly Rate', 'Num Companies Worked', 'Percent Salary Hike', 'Performance Rating',
        'Relationship Satisfaction', 'Stock Option Level', 'Total Working Years',
        'Training Times Last Year', 'Work Life Balance', 'Years At Company',
        'Years In Current Role', 'Years Since Last Promotion', 'Years With Curr Manager',
        'Business Travel', 'Department', 'Education Field', 'Gender', 'Job Role',
        'Marital Status', 'Over Time'
    ]

    available_features = [f for f in features if f in df.columns]
    X = df[available_features].copy()
    y = df['Target']

    # Encoding categorical variables
    encoders = {}
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("==================================================")
    print("2. TRAINING RANDOM FOREST CLASSIFIER MODEL")
    print("==================================================")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf.fit(X_train, y_train)

    # Predictions
    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]

    auc_score = roc_auc_score(y_test, y_prob)
    print(f"Model ROC-AUC Score: {auc_score:.4f}\n")

    print("==================================================")
    print("3. CLASSIFICATION REPORT & METRICS")
    print("==================================================")
    print(classification_report(y_test, y_pred, target_names=['Stayed (0)', 'Left (1)']))

    # Feature Importance Analysis
    importances = pd.DataFrame({
        'Feature': available_features,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("==================================================")
    print("4. TOP 10 PREDICTIVE DRIVERS OF ATTRITION")
    print("==================================================")
    print(importances.head(10).to_string(index=False))

    # Export metrics to reports folder
    os.makedirs("reports", exist_ok=True)
    importances.head(15).to_csv("reports/ml_feature_importances.csv", index=False)
    print("\n[INFO] ML Feature Importances exported to reports/ml_feature_importances.csv")

if __name__ == "__main__":
    train_model()
