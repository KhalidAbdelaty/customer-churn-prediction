-- Feature Extraction Queries
-- Customer Churn Prediction Pipeline

USE customer_churn_db;

-- 1. Customer Segmentation by Value
-- Segments customers into High, Medium, Low value based on total charges
SELECT 
    CASE 
        WHEN total_charges >= 5000 THEN 'High Value'
        WHEN total_charges >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct
FROM customer_complete_profile
GROUP BY customer_segment
ORDER BY avg_monthly_charges DESC;

-- 2. Churn Rate by Contract Type
SELECT 
    contract_type,
    COUNT(*) as total_customers,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(tenure_months), 1) as avg_tenure,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- 3. Service Adoption Impact on Churn
SELECT 
    total_services,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY total_services
ORDER BY total_services;

-- 4. Payment Method Analysis
SELECT 
    payment_method,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- 5. Tenure-based Churn Analysis
SELECT 
    CASE 
        WHEN tenure_months < 12 THEN '0-1 year'
        WHEN tenure_months < 24 THEN '1-2 years'
        WHEN tenure_months < 48 THEN '2-4 years'
        ELSE '4+ years'
    END AS tenure_group,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY tenure_group
ORDER BY 
    CASE 
        WHEN tenure_months < 12 THEN 1
        WHEN tenure_months < 24 THEN 2
        WHEN tenure_months < 48 THEN 3
        ELSE 4
    END;

-- 6. Internet Service Type Impact
SELECT 
    internet_service,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges,
    ROUND(AVG(total_services), 1) as avg_services
FROM customer_complete_profile
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;

-- 7. Senior Citizen Analysis
SELECT 
    CASE senior_citizen 
        WHEN 1 THEN 'Senior'
        ELSE 'Non-Senior'
    END AS customer_type,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(tenure_months), 1) as avg_tenure,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY senior_citizen;

-- 8. Family Status Impact
SELECT 
    CASE 
        WHEN has_partner = 1 AND has_dependents = 1 THEN 'Family'
        WHEN has_partner = 1 THEN 'Couple'
        WHEN has_dependents = 1 THEN 'Single Parent'
        ELSE 'Single'
    END AS family_status,
    COUNT(*) as customer_count,
    SUM(churn) as churned,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) as churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_charges
FROM customer_complete_profile
GROUP BY family_status
ORDER BY churn_rate_pct DESC;

-- 9. Create Feature Matrix for ML
-- This query creates a comprehensive feature set for each customer
CREATE OR REPLACE VIEW ml_feature_matrix AS
SELECT 
    c.customer_id,
    
    -- Demographic features
    CASE WHEN c.gender = 'Male' THEN 1 ELSE 0 END as is_male,
    c.senior_citizen,
    c.has_partner,
    c.has_dependents,
    
    -- Tenure features
    c.tenure_months,
    ROUND(c.tenure_months / 12.0, 2) as tenure_years,
    CASE WHEN c.tenure_months > 24 THEN 1 ELSE 0 END as is_long_term,
    
    -- Service features
    s.phone_service,
    CASE 
        WHEN s.internet_service = 'No' THEN 0
        WHEN s.internet_service = 'DSL' THEN 1
        WHEN s.internet_service = 'Fiber optic' THEN 2
    END as internet_service_type,
    s.total_services,
    s.has_streaming,
    s.has_security,
    s.has_support,
    
    -- Contract features
    CASE 
        WHEN s.contract_type = 'Month-to-month' THEN 0
        WHEN s.contract_type = 'One year' THEN 1
        WHEN s.contract_type = 'Two year' THEN 2
    END as contract_level,
    s.paperless_billing,
    
    -- Billing features
    b.monthly_charges,
    b.total_charges,
    b.avg_monthly_spend,
    b.charge_per_tenure,
    b.auto_payment,
    
    -- Derived features
    CASE WHEN c.has_partner = 1 OR c.has_dependents = 1 THEN 1 ELSE 0 END as has_family,
    CASE WHEN b.monthly_charges > 70 THEN 1 ELSE 0 END as high_monthly_charges,
    CASE WHEN s.total_services >= 4 THEN 1 ELSE 0 END as multi_service_user,
    
    -- Target
    f.churn as target_churn
    
FROM customers c
JOIN service_subscriptions s ON c.customer_id = s.customer_id
JOIN billing_info b ON c.customer_id = b.customer_id
JOIN churn_features f ON c.customer_id = f.customer_id;

-- 10. Identify At-Risk Customers
-- Customers with high churn probability based on historical patterns
CREATE OR REPLACE VIEW at_risk_customers AS
SELECT 
    customer_id,
    tenure_months,
    contract_level,
    total_services,
    monthly_charges,
    has_family,
    
    -- Risk score calculation
    (
        (CASE WHEN tenure_months < 12 THEN 3 ELSE 0 END) +
        (CASE WHEN contract_level = 0 THEN 3 ELSE 0 END) +
        (CASE WHEN total_services < 2 THEN 2 ELSE 0 END) +
        (CASE WHEN has_family = 0 THEN 1 ELSE 0 END) +
        (CASE WHEN monthly_charges > 70 AND total_services < 3 THEN 2 ELSE 0 END)
    ) as risk_score,
    
    CASE 
        WHEN (
            (CASE WHEN tenure_months < 12 THEN 3 ELSE 0 END) +
            (CASE WHEN contract_level = 0 THEN 3 ELSE 0 END) +
            (CASE WHEN total_services < 2 THEN 2 ELSE 0 END) +
            (CASE WHEN has_family = 0 THEN 1 ELSE 0 END) +
            (CASE WHEN monthly_charges > 70 AND total_services < 3 THEN 2 ELSE 0 END)
        ) >= 6 THEN 'High Risk'
        WHEN (
            (CASE WHEN tenure_months < 12 THEN 3 ELSE 0 END) +
            (CASE WHEN contract_level = 0 THEN 3 ELSE 0 END) +
            (CASE WHEN total_services < 2 THEN 2 ELSE 0 END) +
            (CASE WHEN has_family = 0 THEN 1 ELSE 0 END) +
            (CASE WHEN monthly_charges > 70 AND total_services < 3 THEN 2 ELSE 0 END)
        ) >= 3 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_category,
    
    target_churn as actual_churn
    
FROM ml_feature_matrix
ORDER BY risk_score DESC;

-- Summary: Show view information
SELECT 'Feature extraction queries completed' AS status;
SELECT 'Views created: ml_feature_matrix, at_risk_customers' AS info;
