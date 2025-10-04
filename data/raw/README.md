# Raw Data Directory

## Purpose
This directory contains the original, unmodified dataset used in this project.

## Dataset
**File**: `customer_behavior.csv`  
**Source**: Telco Customer Churn Dataset  
**Size**: ~7,000 customer records  
**Format**: CSV

## Download Instructions

Due to GitHub's file size limitations, the dataset is not included in this repository.

### Option 1: Use Sample Dataset
Download the Telco Customer Churn dataset from:
- [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Or use the file from your local copy

### Option 2: Use Your Own Data
If using your own dataset, ensure it has the following columns:
- `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`
- `tenure`, `PhoneService`, `MultipleLines`, `InternetService`
- `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`
- `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`
- `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `Churn`

## Usage

1. Place your CSV file here
2. Rename it to `customer_behavior.csv`
3. Run the notebooks in order

## Note
⚠️ **Do not commit actual data files to GitHub** (they're excluded via .gitignore)
