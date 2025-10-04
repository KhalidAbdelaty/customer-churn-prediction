-- Database Initialization Script
-- Customer Churn Prediction Pipeline

-- Create database
CREATE DATABASE IF NOT EXISTS customer_churn_db;
USE customer_churn_db;

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Drop views if they exist
DROP VIEW IF EXISTS at_risk_customers;
DROP VIEW IF EXISTS ml_feature_matrix;
DROP VIEW IF EXISTS high_risk_customers;
DROP VIEW IF EXISTS churn_statistics;
DROP VIEW IF EXISTS customer_complete_profile;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS churn_features;
DROP TABLE IF EXISTS billing_info;
DROP TABLE IF EXISTS service_subscriptions;
DROP TABLE IF EXISTS customers;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Main customers table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    senior_citizen TINYINT,
    has_partner TINYINT,
    has_dependents TINYINT,
    tenure_months INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenure (tenure_months),
    INDEX idx_senior (senior_citizen)
);

-- Service subscriptions table
CREATE TABLE service_subscriptions (
    customer_id VARCHAR(20) PRIMARY KEY,
    phone_service TINYINT,
    internet_service VARCHAR(20),
    contract_type VARCHAR(20),
    paperless_billing TINYINT,
    total_services INT,
    has_streaming TINYINT,
    has_security TINYINT,
    has_support TINYINT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_contract (contract_type),
    INDEX idx_internet (internet_service)
);

-- Billing information table
CREATE TABLE billing_info (
    customer_id VARCHAR(20) PRIMARY KEY,
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(10, 2),
    payment_method VARCHAR(50),
    auto_payment TINYINT,
    avg_monthly_spend DECIMAL(10, 2),
    charge_per_tenure DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_monthly_charges (monthly_charges),
    INDEX idx_payment_method (payment_method)
);

-- Churn features table (includes target variable)
CREATE TABLE churn_features (
    customer_id VARCHAR(20) PRIMARY KEY,
    is_long_term TINYINT,
    has_partner_or_dependent TINYINT,
    churn TINYINT,
    churn_probability DECIMAL(5, 4) DEFAULT NULL,
    prediction_date TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_churn (churn),
    INDEX idx_long_term (is_long_term)
);

-- Create a view for complete customer profile
CREATE OR REPLACE VIEW customer_complete_profile AS
SELECT 
    c.customer_id,
    c.gender,
    c.senior_citizen,
    c.has_partner,
    c.has_dependents,
    c.tenure_months,
    s.phone_service,
    s.internet_service,
    s.contract_type,
    s.paperless_billing,
    s.total_services,
    s.has_streaming,
    s.has_security,
    s.has_support,
    b.monthly_charges,
    b.total_charges,
    b.payment_method,
    b.auto_payment,
    b.avg_monthly_spend,
    b.charge_per_tenure,
    f.is_long_term,
    f.has_partner_or_dependent,
    f.churn,
    f.churn_probability
FROM customers c
LEFT JOIN service_subscriptions s ON c.customer_id = s.customer_id
LEFT JOIN billing_info b ON c.customer_id = b.customer_id
LEFT JOIN churn_features f ON c.customer_id = f.customer_id;

-- Summary statistics view
CREATE OR REPLACE VIEW churn_statistics AS
SELECT 
    COUNT(*) as total_customers,
    SUM(churn) as churned_customers,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(tenure_months), 2) as avg_tenure_months,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges,
    ROUND(AVG(total_charges), 2) as avg_total_charges
FROM customer_complete_profile;

-- High risk customers view
CREATE OR REPLACE VIEW high_risk_customers AS
SELECT 
    customer_id,
    tenure_months,
    monthly_charges,
    contract_type,
    total_services,
    churn
FROM customer_complete_profile
WHERE 
    (tenure_months < 12 AND contract_type = 'Month-to-month')
    OR (total_services < 2)
    OR (monthly_charges > 70 AND total_services < 3)
ORDER BY tenure_months ASC;

SHOW TABLES;
