import pandas as pd
from datetime import datetime, timedelta
import logging
import json

class CustomerDataCollector:
    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string
        self.logger = logging.getLogger(__name__)
        
        # Validate connection string
        if not db_connection_string:
            self.logger.error("No database connection string provided")
            raise ValueError("Database connection string is required. Please configure your database connection.")
    
    def _get_connection(self):
        """
        Establish a secure connection to the database
        """
        try:
            from sqlalchemy import create_engine
            
            # Create engine with appropriate security settings
            engine = create_engine(
                self.db_connection_string,
                connect_args={"check_same_thread": False} if "sqlite" in self.db_connection_string else {
                    "sslmode": "require"  # Enforce SSL for PostgreSQL
                }
            )
            
            # Test connection
            with engine.connect() as conn:
                pass
                
            return engine
        except ImportError as e:
            self.logger.error("SQLAlchemy is not installed")
            raise ConnectionError("Database connection failed: SQLAlchemy is required but not installed.")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise ConnectionError(f"Database connection failed: {str(e)}. Please check your database credentials.")
    
    def collect_customer_data(self):
        """
        Collect customer data from the database
        """
        try:
            import pandas as pd
            
            engine = self._get_connection()
            
            # Use parameterized query to prevent SQL injection
            query = """
            SELECT c.* 
            FROM customers c
            """
            
            self.logger.info("Collecting customer data")
            df = pd.read_sql(query, engine)
            
            self.logger.info(f"Collected data for {len(df)} customers")
            return df
        except Exception as e:
            self.logger.error(f"Error collecting customer data: {str(e)}")
            raise
    
    def collect_transaction_data(self, time_period=365):
        """
        Collect transaction data from the database
        
        Args:
            time_period (int): Number of days to look back
        """
        try:
            import pandas as pd
            from datetime import datetime, timedelta
            
            engine = self._get_connection()
            
            # Calculate cutoff date
            cutoff_date = (datetime.now() - timedelta(days=time_period)).strftime('%Y-%m-%d')
            
            # Use parameterized query to prevent SQL injection
            query = """
            SELECT t.*, p.name as product_name, p.category, p.price
            FROM transactions t
            JOIN products p ON t.product_id = p.product_id
            WHERE t.purchase_date >= ?
            """
            
            self.logger.info(f"Collecting transaction data for the last {time_period} days")
            df = pd.read_sql(query, engine, params=[cutoff_date])
            
            self.logger.info(f"Collected {len(df)} transactions")
            return df
        except Exception as e:
            self.logger.error(f"Error collecting transaction data: {str(e)}")
            raise
    
    def test_connection(self):
        """
        Test the database connection and return diagnostic information
        """
        try:
            engine = self._get_connection()
            
            # Check if required tables exist
            tables_to_check = ['customers', 'transactions', 'products']
            missing_tables = []
            
            from sqlalchemy import inspect
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            for table in tables_to_check:
                if table not in existing_tables:
                    missing_tables.append(table)
            
            if missing_tables:
                return {
                    'success': False,
                    'message': f"Connected to database, but missing required tables: {', '.join(missing_tables)}",
                    'missing_tables': missing_tables
                }
            
            # Check if tables have data
            empty_tables = []
            for table in tables_to_check:
                count_query = f"SELECT COUNT(*) FROM {table}"
                count = engine.execute(count_query).scalar()
                if count == 0:
                    empty_tables.append(table)
            
            if empty_tables:
                return {
                    'success': True,
                    'warning': f"Tables exist but contain no data: {', '.join(empty_tables)}",
                    'empty_tables': empty_tables
                }
            
            return {
                'success': True,
                'message': "Successfully connected to database. All required tables exist and contain data."
            }
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return {
                'success': False,
                'message': f"Failed to connect to database: {str(e)}",
                'error': str(e)
            }