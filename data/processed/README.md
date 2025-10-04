# Processed Data Directory

## Purpose
This directory contains cleaned and preprocessed data ready for modeling.

## Generated Files
After running the preprocessing notebook (`02_preprocessing.ipynb`), you'll find:

- `customer_churn_processed.csv` - Cleaned dataset with engineered features

## Features Included

### Original Features (Encoded)
- Customer demographics
- Service subscriptions
- Contract details
- Billing information

### Engineered Features
- `tenure_years` - Tenure in years
- `avg_monthly_spend` - Average monthly spending
- `charge_per_tenure` - Monthly charges normalized by tenure
- `total_services` - Count of active services
- `has_streaming`, `has_security`, `has_support` - Service indicators
- `is_long_term` - Customer with >24 months tenure
- `has_partner_or_dependent` - Family indicator
- `auto_payment` - Automatic payment indicator
- Payment method dummies

### Target Variable
- `churn_encoded` - Binary churn indicator (0/1)

## Data Quality
- ✅ No missing values
- ✅ All data types corrected
- ✅ Categorical variables encoded
- ✅ ~7,000 customer records

## Note
⚠️ **Processed files are not committed to GitHub** (excluded via .gitignore)
