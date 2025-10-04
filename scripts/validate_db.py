import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent))

from utils import query_to_dataframe, get_table_stats

def validate_database():
    print("="*70)
    print("Database Validation Report")
    print("="*70)
    
    print("\n1. Table Row Counts")
    print("-" * 70)
    stats = get_table_stats()
    if stats:
        total_records = stats.get('customers', 0)
        for table, count in stats.items():
            status = "✓" if count == total_records else "✗"
            print(f"  {status} {table:30s} : {count:>6d} rows")
        
        if all(count == total_records for count in stats.values()):
            print("\n  ✓ All tables have consistent record counts")
        else:
            print("\n  ⚠ Warning: Inconsistent record counts detected")
    else:
        print("  ✗ Could not retrieve table statistics")
        return
    
    print("\n2. Data Quality Checks")
    print("-" * 70)
    
    # Check for nulls in critical fields
    null_check_query = """
        SELECT 
            SUM(CASE WHEN tenure_months IS NULL THEN 1 ELSE 0 END) as null_tenure,
            SUM(CASE WHEN monthly_charges IS NULL THEN 1 ELSE 0 END) as null_monthly,
            SUM(CASE WHEN total_charges IS NULL THEN 1 ELSE 0 END) as null_total,
            SUM(CASE WHEN churn IS NULL THEN 1 ELSE 0 END) as null_churn
        FROM customer_complete_profile
    """
    
    null_df = query_to_dataframe(null_check_query)
    if null_df is not None:
        null_counts = null_df.iloc[0]
        if null_counts.sum() == 0:
            print("  ✓ No NULL values in critical fields")
        else:
            print("  ⚠ Found NULL values:")
            for col, count in null_counts.items():
                if count > 0:
                    print(f"    - {col}: {count} nulls")
    
    # Check for duplicate customers
    dup_query = """
        SELECT COUNT(*) - COUNT(DISTINCT customer_id) as duplicates
        FROM customers
    """
    dup_df = query_to_dataframe(dup_query)
    if dup_df is not None:
        dup_count = dup_df.iloc[0, 0]
        if dup_count == 0:
            print("  ✓ No duplicate customer IDs")
        else:
            print(f"  ✗ Found {dup_count} duplicate customer IDs")
    
    # Check data ranges
    range_query = """
        SELECT 
            MIN(tenure_months) as min_tenure,
            MAX(tenure_months) as max_tenure,
            MIN(monthly_charges) as min_monthly,
            MAX(monthly_charges) as max_monthly,
            MIN(total_charges) as min_total,
            MAX(total_charges) as max_total
        FROM customer_complete_profile
    """
    range_df = query_to_dataframe(range_query)
    if range_df is not None:
        print("  ✓ Data ranges validated:")
        print(f"    - Tenure: {range_df.iloc[0]['min_tenure']:.0f} - {range_df.iloc[0]['max_tenure']:.0f} months")
        print(f"    - Monthly charges: ${range_df.iloc[0]['min_monthly']:.2f} - ${range_df.iloc[0]['max_monthly']:.2f}")
        print(f"    - Total charges: ${range_df.iloc[0]['min_total']:.2f} - ${range_df.iloc[0]['max_total']:.2f}")
    
    print("\n3. Business Logic Validation")
    print("-" * 70)
    
    # Check if total charges make sense relative to monthly charges
    logic_query = """
        SELECT COUNT(*) as inconsistent_count
        FROM customer_complete_profile
        WHERE total_charges < (monthly_charges * tenure_months * 0.5)
        AND tenure_months > 0
    """
    logic_df = query_to_dataframe(logic_query)
    if logic_df is not None:
        inconsistent = logic_df.iloc[0, 0]
        if inconsistent == 0:
            print("  ✓ Total charges consistent with monthly charges")
        else:
            print(f"  ⚠ {inconsistent} records with potentially inconsistent charges")
    
    # Check service counts
    service_query = """
        SELECT 
            MIN(total_services) as min_services,
            MAX(total_services) as max_services,
            ROUND(AVG(total_services), 2) as avg_services
        FROM customer_complete_profile
    """
    service_df = query_to_dataframe(service_query)
    if service_df is not None:
        print(f"  ✓ Service counts: {service_df.iloc[0]['min_services']:.0f} - {service_df.iloc[0]['max_services']:.0f} " +
              f"(avg: {service_df.iloc[0]['avg_services']:.2f})")
    
    print("\n4. Feature Matrix Validation")
    print("-" * 70)
    
    feature_query = """
        SELECT COUNT(*) as total_records
        FROM ml_feature_matrix
    """
    feature_df = query_to_dataframe(feature_query)
    if feature_df is not None:
        feature_count = feature_df.iloc[0, 0]
        if feature_count == total_records:
            print(f"  ✓ ML feature matrix complete: {feature_count} records")
        else:
            print(f"  ✗ ML feature matrix incomplete: {feature_count}/{total_records} records")
    
    # Check feature distributions
    dist_query = """
        SELECT 
            ROUND(AVG(is_male), 3) as pct_male,
            ROUND(AVG(senior_citizen), 3) as pct_senior,
            ROUND(AVG(has_partner), 3) as pct_partner,
            ROUND(AVG(target_churn), 3) as churn_rate
        FROM ml_feature_matrix
    """
    dist_df = query_to_dataframe(dist_query)
    if dist_df is not None:
        print("  ✓ Feature distributions:")
        print(f"    - Male: {dist_df.iloc[0]['pct_male']*100:.1f}%")
        print(f"    - Senior: {dist_df.iloc[0]['pct_senior']*100:.1f}%")
        print(f"    - Has Partner: {dist_df.iloc[0]['pct_partner']*100:.1f}%")
        print(f"    - Churn Rate: {dist_df.iloc[0]['churn_rate']*100:.1f}%")
    
    print("\n5. View Validation")
    print("-" * 70)
    
    views = [
        'customer_complete_profile',
        'churn_statistics',
        'high_risk_customers',
        'ml_feature_matrix',
        'at_risk_customers'
    ]
    
    for view in views:
        query = f"SELECT COUNT(*) as count FROM {view}"
        df = query_to_dataframe(query)
        if df is not None:
            count = df.iloc[0, 0]
            print(f"  ✓ {view:30s} : {count:>6d} rows")
        else:
            print(f"  ✗ {view:30s} : ERROR")
    
    print("\n" + "="*70)
    print("Validation Complete")
    print("="*70)
    
    print("\nSummary:")
    print("  - All critical checks passed" if stats else "  - Some checks failed")
    print("  - Database is ready for model training" if stats else "  - Please review errors above")
    print("="*70)

if __name__ == "__main__":
    validate_database()
