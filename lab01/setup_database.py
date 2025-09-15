"""
Database Setup Script for University Performance Analysis
This script helps set up the PostgreSQL database and initial configuration
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    """Create the university_db database if it doesn't exist"""
    
    # Get database connection details
    print("🔧 Database Setup for University Performance Analysis")
    print("=" * 50)
    
    # Default connection parameters (update these for your setup)
    host = input("Enter PostgreSQL host (default: localhost): ").strip() or "localhost"
    port = input("Enter PostgreSQL port (default: 5432): ").strip() or "5432"
    user = input("Enter PostgreSQL username (default: postgres): ").strip() or "postgres"
    password = input("Enter PostgreSQL password: ").strip()
    
    if not password:
        print("❌ Password is required!")
        return False
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        print("🔄 Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if uni exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'uni'")
        exists = cursor.fetchone()
        
        if exists:
            print("✅ Database 'uni' already exists")
        else:
            # Create the database
            print("🔄 Creating database 'uni'...")
            cursor.execute("CREATE DATABASE uni")
            print("✅ Database 'uni' created successfully")
        
        cursor.close()
        conn.close()
        
        # Test connection to the new database
        print("🔄 Testing connection to uni...")
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='uni'
        )
        test_conn.close()
        print("✅ Connection to uni successful")
        
        # Create configuration file
        config_content = f"""# Database Configuration for University Performance Analysis
# Update these values according to your PostgreSQL setup

DB_CONFIG = {{
    'host': '{host}',
    'database': 'uni',
    'user': '{user}',
    'password': '{password}',
    'port': {port}
}}
"""
        
        with open('db_config.py', 'w') as f:
            f.write(config_content)
        
        print("✅ Configuration file 'db_config.py' created")
        print("\n🎉 Database setup complete!")
        print("\nNext steps:")
        print("1. Install required packages: pip install -r requirements.txt")
        print("2. Run the main analysis: python university_db_performance.py")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main setup function"""
    success = create_database()
    
    if not success:
        print("\n❌ Setup failed. Please check your PostgreSQL configuration and try again.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")

if __name__ == "__main__":
    main()
