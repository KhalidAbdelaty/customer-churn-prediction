import sys
from pathlib import Path
import mysql.connector
from mysql.connector import Error

sys.path.append(str(Path(__file__).parent))

from utils import load_config

def cleanup_database():
    print("="*70)
    print("Database Cleanup Utility")
    print("="*70)
    
    config = load_config()
    db_config = config['database']
    
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        cursor = connection.cursor()
        
        print(f"\nConnecting to database: {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
        
        print("\nDisabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        print("\nDropping views...")
        views = ['at_risk_customers', 'ml_feature_matrix', 'high_risk_customers', 
                 'churn_statistics', 'customer_complete_profile']
        
        for view in views:
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view}")
                print(f"  ✓ Dropped view: {view}")
            except Error as e:
                print(f"  ✗ Error dropping {view}: {e}")
        
        print("\nDropping tables...")
        tables = ['churn_features', 'billing_info', 'service_subscriptions', 'customers']
        
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  ✓ Dropped table: {table}")
            except Error as e:
                print(f"  ✗ Error dropping {table}: {e}")
        
        print("\nRe-enabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        
        print("\n" + "="*70)
        print("Cleanup Complete!")
        print("="*70)
        print("\nYou can now run: python load_data_to_db.py")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\nError during cleanup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    cleanup_database()
