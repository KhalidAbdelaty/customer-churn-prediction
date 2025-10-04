import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path, 'r') as f:
        return json.load(f)

def get_db_connection():
    config = load_config()
    db_config = config['database']
    
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            autocommit=False
        )
        if connection.is_connected():
            return connection
    except Error as e:
        # Try without database specified (for initial setup)
        try:
            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                autocommit=False
            )
            if connection.is_connected():
                return connection
        except Error as e2:
            print(f"Error connecting to MySQL: {e}")
            return None

def execute_sql_file(sql_file_path):
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Remove comments and split into statements
        statements = []
        current = []
        
        for line in sql_content.split('\n'):
            stripped = line.strip()
            
            # Skip comment lines
            if stripped.startswith('--') or not stripped:
                continue
            
            # Remove inline comments
            if '--' in stripped:
                stripped = stripped[:stripped.index('--')].strip()
            
            current.append(stripped)
            
            # End of statement
            if stripped.endswith(';'):
                statement = ' '.join(current).strip()
                if statement:
                    statements.append(statement)
                current = []
        
        # Execute each statement
        for statement in statements:
            try:
                cursor.execute(statement)
                
                # Try to fetch results if any
                try:
                    cursor.fetchall()
                except:
                    pass
                
            except Error as e:
                error_msg = str(e).lower()
                # Only show warnings for real errors
                if 'already exists' not in error_msg and "doesn't exist" not in error_msg:
                    print(f"Warning: {e}")
        
        connection.commit()
        print(f"Successfully executed: {sql_file_path}")
        return True
        
    except Error as e:
        print(f"Error executing SQL file: {e}")
        if connection:
            try:
                connection.rollback()
            except:
                pass
        return False
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if connection:
            try:
                if connection.is_connected():
                    connection.close()
            except:
                pass

def load_data_to_db(csv_file_path):
    df = pd.read_csv(csv_file_path)
    connection = get_db_connection()
    
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Insert into customers table
        for _, row in df.iterrows():
            customer_query = """
                INSERT INTO customers 
                (customer_id, gender, senior_citizen, has_partner, has_dependents, tenure_months)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                tenure_months = VALUES(tenure_months)
            """
            
            gender = 'Male' if row['gender_encoded'] == 1 else 'Female'
            
            cursor.execute(customer_query, (
                row['customerID'],
                gender,
                int(row['SeniorCitizen']),
                int(row['partner_encoded']),
                int(row['dependents_encoded']),
                int(row['tenure'])
            ))
        
        # Insert into service_subscriptions table
        for _, row in df.iterrows():
            contract_map = {0: 'Month-to-month', 1: 'One year', 2: 'Two year'}
            internet_map = {0: 'No', 1: 'DSL', 2: 'Fiber optic'}
            
            service_query = """
                INSERT INTO service_subscriptions
                (customer_id, phone_service, internet_service, contract_type, paperless_billing,
                 total_services, has_streaming, has_security, has_support)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                total_services = VALUES(total_services)
            """
            
            cursor.execute(service_query, (
                row['customerID'],
                int(row['phone_service_encoded']),
                internet_map.get(int(row['internet_service_encoded']), 'No'),
                contract_map.get(int(row['contract_encoded']), 'Month-to-month'),
                int(row['paperless_billing_encoded']),
                int(row['total_services']),
                int(row['has_streaming']),
                int(row['has_security']),
                int(row['has_support'])
            ))
        
        # Insert into billing_info table
        for _, row in df.iterrows():
            payment_cols = [col for col in df.columns if col.startswith('payment_')]
            payment_method = 'Electronic check'
            
            for col in payment_cols:
                if row[col] == 1:
                    payment_method = col.replace('payment_', '').replace('_', ' ')
                    break
            
            billing_query = """
                INSERT INTO billing_info
                (customer_id, monthly_charges, total_charges, payment_method, 
                 auto_payment, avg_monthly_spend, charge_per_tenure)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                monthly_charges = VALUES(monthly_charges)
            """
            
            cursor.execute(billing_query, (
                row['customerID'],
                float(row['MonthlyCharges']),
                float(row['TotalCharges']),
                payment_method,
                int(row['auto_payment']),
                float(row['avg_monthly_spend']),
                float(row['charge_per_tenure'])
            ))
        
        # Insert into churn_features table
        for _, row in df.iterrows():
            churn_query = """
                INSERT INTO churn_features
                (customer_id, is_long_term, has_partner_or_dependent, churn)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                churn = VALUES(churn)
            """
            
            cursor.execute(churn_query, (
                row['customerID'],
                int(row['is_long_term']),
                int(row['has_partner_or_dependent']),
                int(row['churn_encoded'])
            ))
        
        connection.commit()
        print(f"Successfully loaded {len(df)} records into database")
        return True
        
    except Error as e:
        print(f"Error loading data: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def query_to_dataframe(query):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def get_table_stats():
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        
        tables = ['customers', 'service_subscriptions', 'billing_info', 'churn_features']
        stats = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            stats[table] = count
        
        return stats
        
    except Error as e:
        print(f"Error getting stats: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Database utility functions loaded successfully")
    
    connection = get_db_connection()
    if connection:
        print("✓ Database connection successful")
        connection.close()
    else:
        print("✗ Database connection failed")
