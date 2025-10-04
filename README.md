# 🎯 Milestone 1: Data Collection & Feature Engineering

**AI-Enhanced Data Pipeline for Customer Churn Prediction**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Database Schema](#️-database-schema)
- [Results](#-results)
- [Technologies](#️-technologies)
- [Next Steps](#-next-steps-milestone-2)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

This project implements a comprehensive data pipeline for customer churn prediction in the telecommunications industry. It focuses on data collection, cleaning, feature engineering, and database design to prepare data for machine learning models.

### Key Objectives
- ✅ Collect and validate customer behavioral data
- ✅ Clean and preprocess ~7,000 customer records
- ✅ Engineer 15+ predictive features
- ✅ Design normalized database schema (4 tables)
- ✅ Create analytical SQL views for insights
- ✅ Automate entire pipeline with Python scripts

### Business Impact
- **26.54% churn rate** identified
- **42.71% churn** in month-to-month contracts
- **2,029 high-risk customers** flagged for intervention
- Clear actionable insights for retention strategies

---

## 📁 Project Structure

```
milestone_1/
├── data/
│   ├── raw/                        # Original unmodified data
│   │   ├── README.md              # Data source information
│   │   └── .gitkeep               # Keep directory in Git
│   └── processed/                  # Cleaned and processed data
│       ├── README.md              # Processing details
│       └── .gitkeep               # Keep directory in Git
│
├── sql_queries/
│   ├── db_init.sql                # Database schema creation
│   └── feature_extraction.sql     # Analytical queries
│
├── notebooks/
│   ├── 01_data_exploration.ipynb  # Exploratory Data Analysis
│   └── 02_preprocessing.ipynb     # Data cleaning & feature engineering
│
├── scripts/
│   ├── utils.py                   # Database utility functions
│   ├── load_data_to_db.py        # Data loading automation
│   ├── validate_db.py            # Data quality validation
│   └── cleanup_db.py             # Database maintenance
│
├── .gitignore                     # Git ignore rules
├── config.template.json           # Configuration template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## ✨ Features

### Data Processing
- **Automated data cleaning** - Handles missing values, type conversions
- **Feature engineering** - Creates 15+ predictive features
- **Data validation** - Multiple quality checkpoints

### Database Design
- **Normalized schema** - 4 tables with proper relationships
- **Optimized indexing** - Fast query performance
- **Analytical views** - Pre-built queries for insights

### Analysis Tools
- **Exploratory analysis** - Jupyter notebooks with visualizations
- **SQL queries** - Customer segmentation, churn patterns
- **Risk scoring** - Identifies high-risk customers

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Jupyter Notebook/Lab

### Step 1: Clone Repository
```bash
git clone https://github.com/KhalidAbdelaty/customer-churn-prediction.git
cd customer-churn-prediction/milestone_1
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database
```bash
# Copy template config
cp config.template.json config.json

# Edit config.json with your MySQL credentials
nano config.json
```

### Step 4: Prepare Data
- Download the Telco Customer Churn dataset
- Place in `data/raw/` as `customer_behavior.csv`

---

## 💻 Usage

### Run Complete Pipeline
```bash
cd scripts

# 1. Run data exploration
jupyter notebook ../notebooks/01_data_exploration.ipynb

# 2. Run preprocessing
jupyter notebook ../notebooks/02_preprocessing.ipynb

# 3. Load data to database
python load_data_to_db.py

# 4. Validate data quality
python validate_db.py
```

### Individual Steps

**Data Exploration:**
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

**Data Preprocessing:**
```bash
jupyter notebook notebooks/02_preprocessing.ipynb
```

**Database Setup:**
```bash
python scripts/load_data_to_db.py
```

**Validation:**
```bash
python scripts/validate_db.py
```

---

## 🗄️ Database Schema

### Tables

**1. customers**
- `customer_id` (PK)
- `gender`, `senior_citizen`, `has_partner`, `has_dependents`
- `tenure_months`

**2. service_subscriptions**
- `customer_id` (PK, FK)
- `phone_service`, `internet_service`, `contract_type`
- `total_services`, `has_streaming`, `has_security`, `has_support`

**3. billing_info**
- `customer_id` (PK, FK)
- `monthly_charges`, `total_charges`, `payment_method`
- `auto_payment`, `avg_monthly_spend`, `charge_per_tenure`

**4. churn_features**
- `customer_id` (PK, FK)
- `is_long_term`, `has_partner_or_dependent`
- `churn`, `churn_probability`

### Views

- `customer_complete_profile` - Joined customer data
- `churn_statistics` - Overall churn metrics
- `high_risk_customers` - Customers at risk
- `ml_feature_matrix` - ML-ready features
- `at_risk_customers` - Risk-scored customers

---

## 📊 Results

### Data Quality
- ✅ **7,043 customer records** processed
- ✅ **Zero missing values** in critical fields
- ✅ **Zero duplicates** detected
- ✅ **15+ engineered features** created

### Key Insights

**Churn Rate by Contract Type:**
| Contract | Customers | Churn Rate |
|----------|-----------|------------|
| Month-to-month | 3,875 (55%) | **42.71%** |
| One year | 1,473 (21%) | **11.27%** |
| Two year | 1,695 (24%) | **2.83%** |

**Risk Distribution:**
- High Risk: 2,029 customers (28.8%)
- Medium Risk: 2,235 customers (31.7%)
- Low Risk: 2,779 customers (39.5%)

**Feature Importance (Preview):**
1. Contract type (huge impact)
2. Tenure (first 6-12 months critical)
3. Service count (engagement indicator)

---

## 🛠️ Technologies

### Languages & Tools
- **Python 3.8+** - Data processing and automation
- **MySQL 8.0+** - Database management
- **Jupyter** - Interactive analysis

### Python Libraries
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib`, `seaborn` - Visualization
- `mysql-connector-python` - Database connectivity
- `scikit-learn` - Preprocessing utilities

---

## 📈 Next Steps (Milestone 2)

- [ ] Model selection (XGBoost, Random Forest, Logistic Regression)
- [ ] Model training and hyperparameter tuning
- [ ] Performance evaluation (Accuracy, Precision, Recall, F1)
- [ ] Inference pipeline development
- [ ] Batch prediction implementation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Telco Customer Churn Dataset from Kaggle
- AI & Data Science Track - Round 3 Project

---

**⭐ If you find this project useful, please consider giving it a star!**
```
git commit -m "docs: Fix Table of Contents hyperlinks and update repository URL"
git push origin main
```
