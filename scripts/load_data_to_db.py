import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import (
    load_config, 
    execute_sql_file, 
    load_data_to_db, 
    get_table_stats,
    query_to_dataframe
)

def main():
    print("="*70)
    print("Customer Churn Database Setup")
    print("="*70)
    
    config = load_config()
    
    # Paths
    sql_dir = Path(config['paths']['sql_queries'])
    processed_dir = Path(config['paths']['processed_data'])
    
    db_init_sql = sql_dir / 'db_init.sql'
    feature_sql = sql_dir / 'feature_extraction.sql'
    processed_csv = processed_dir / 'customer_churn_processed.csv'
    
    print("\n[1/4] Initializing database schema...")
    if db_init_sql.exists():
        if execute_sql_file(db_init_sql):
            print("✓ Database schema created successfully")
        else:
            print("✗ Failed to create database schema")
            return
    else:
        print(f"✗ SQL file not found: {db_init_sql}")
        return
    
    print("\n[2/4] Loading processed data into database...")
    if processed_csv.exists():
        if load_data_to_db(processed_csv):
            print("✓ Data loaded successfully")
        else:
            print("✗ Failed to load data")
            return
    else:
        print(f"✗ Processed data file not found: {processed_csv}")
        print("Please run the preprocessing notebook first")
        return
    
    print("\n[3/4] Creating feature extraction views...")
    if feature_sql.exists():
        if execute_sql_file(feature_sql):
            print("✓ Feature extraction views created")
        else:
            print("✗ Failed to create views")
            return
    else:
        print(f"✗ SQL file not found: {feature_sql}")
        return
    
    print("\n[4/4] Verifying data integrity...")
    stats = get_table_stats()
    if stats:
        print("\nTable Statistics:")
        print("-" * 50)
        for table, count in stats.items():
            print(f"  {table:30s} : {count:>6d} rows")
        print("-" * 50)
        
        if all(count > 0 for count in stats.values()):
            print("✓ All tables populated successfully")
        else:
            print("⚠ Some tables are empty")
    else:
        print("✗ Could not retrieve table statistics")
        return
    
    print("\n" + "="*70)
    print("Database Setup Complete!")
    print("="*70)
    
    print("\nSample Query Results:")
    print("-" * 70)
    
    query = "SELECT * FROM churn_statistics"
    df = query_to_dataframe(query)
    if df is not None:
        print("\nChurn Statistics:")
        print(df.to_string(index=False))
    
    query = """
        SELECT risk_category, COUNT(*) as count 
        FROM at_risk_customers 
        GROUP BY risk_category 
        ORDER BY 
            CASE risk_category 
                WHEN 'High Risk' THEN 1 
                WHEN 'Medium Risk' THEN 2 
                ELSE 3 
            END
    """
    df = query_to_dataframe(query)
    if df is not None:
        print("\nRisk Distribution:")
        print(df.to_string(index=False))
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("  1. Review the data in MySQL Workbench or command line")
    print("  2. Run feature extraction queries for analysis")
    print("  3. Proceed to Milestone 2: AI Model Integration")
    print("="*70)

if __name__ == "__main__":
    main()
