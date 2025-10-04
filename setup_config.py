import os
import sys
import json
from pathlib import Path

def setup_config():
    print("=== AI-Enhanced Data Pipeline - Configuration Setup ===\n")
    
    base_dir = Path(r"C:\Users\Khalid Abdelaty\depii r3\milestone_1")
    
    if not base_dir.exists():
        print(f"Error: Directory {base_dir} does not exist.")
        print("Please run setup_project.bat first!")
        return
    
    config = {
        "database": {
            "host": "localhost",
            "port": 3306,
            "user": "",
            "password": "",
            "database": "customer_churn_db"
        },
        "paths": {
            "raw_data": str(base_dir / "data" / "raw"),
            "processed_data": str(base_dir / "data" / "processed"),
            "sql_queries": str(base_dir / "sql_queries"),
            "notebooks": str(base_dir / "notebooks")
        }
    }
    
    print("MySQL Database Configuration")
    print("-" * 40)
    config["database"]["user"] = input("MySQL Username (default: root): ").strip() or "root"
    config["database"]["password"] = input("MySQL Password: ").strip()
    
    db_name = input("Database Name (default: customer_churn_db): ").strip()
    if db_name:
        config["database"]["database"] = db_name
    
    config_path = base_dir / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"\n✓ Configuration saved to: {config_path}")
    
    print("\n=== Checking Python Environment ===")
    required_packages = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "mysql-connector-python",
        "scikit-learn",
        "jupyter"
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == "mysql-connector-python":
                __import__("mysql.connector")
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print("\n⚠ Missing packages detected!")
        print("Install them with:")
        print(f"pip install {' '.join(missing)}")
    else:
        print("\n✓ All required packages are installed!")
    
    print("\n=== Setup Complete ===")
    print(f"Project root: {base_dir}")
    print("\nNext steps:")
    print("1. Place your CSV file in: data\\raw\\")
    print("2. Run the Jupyter notebooks in order")
    print("3. Execute SQL scripts to set up the database")

if __name__ == "__main__":
    setup_config()
