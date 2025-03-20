import sqlite3
import pandas as pd
from sqlalchemy import create_engine

class Database:
    def __init__(self, config):
        self.config = config
        self.engine = self._create_engine()
        
    def _create_engine(self):
        """Create SQLAlchemy engine based on configuration"""
        db_type = self.config.get('db_type', 'sqlite')
        
        if db_type == 'sqlite':
            database = self.config.get('database', 'database.db')
            return create_engine(f'sqlite:///{database}')
        
        elif db_type == 'postgresql':
            host = self.config.get('host', 'localhost')
            database = self.config.get('database')
            username = self.config.get('username')
            password = self.config.get('password')
            return create_engine(f'postgresql://{username}:{password}@{host}/{database}')
        
        elif db_type == 'mysql':
            host = self.config.get('host', 'localhost')
            database = self.config.get('database')
            username = self.config.get('username')
            password = self.config.get('password')
            return create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                pass
            return True
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")
    
    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        try:
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")
    
    def get_tables(self):
        """Get list of tables in the database"""
        if self.config.get('db_type') == 'sqlite':
            query = "SELECT name FROM sqlite_master WHERE type='table';"
        elif self.config.get('db_type') == 'postgresql':
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        elif self.config.get('db_type') == 'mysql':
            query = "SHOW TABLES;"
        else:
            raise ValueError(f"Unsupported database type: {self.config.get('db_type')}")
        
        result = self.execute_query(query)
        return result.iloc[:, 0].tolist()
    
    def get_table_schema(self, table_name):
        """Get schema for a specific table"""
        if self.config.get('db_type') == 'sqlite':
            query = f"PRAGMA table_info({table_name});"
            result = self.execute_query(query)
            return result[['name', 'type']]
        elif self.config.get('db_type') == 'postgresql':
            query = f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}';
            """
            return self.execute_query(query)
        elif self.config.get('db_type') == 'mysql':
            query = f"DESCRIBE {table_name};"
            result = self.execute_query(query)
            return result[['Field', 'Type']]
        else:
            raise ValueError(f"Unsupported database type: {self.config.get('db_type')}")
    
    def get_sample_data(self, table_name, limit=5):
        """Get sample data from a table"""
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        return self.execute_query(query)
    
    def get_table_count(self, table_name):
        """Get row count for a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name};"
        result = self.execute_query(query)
        return result.iloc[0, 0]
    
    def get_database_info(self):
        """Get general information about the database"""
        tables = self.get_tables()
        info = {
            'database_type': self.config.get('db_type'),
            'database_name': self.config.get('database'),
            'tables': []
        }
        
        for table in tables:
            table_info = {
                'name': table,
                'row_count': self.get_table_count(table),
                'schema': self.get_table_schema(table).to_dict('records')
            }
            info['tables'].append(table_info)
        
        return info