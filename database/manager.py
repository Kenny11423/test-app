# File: database/manager.py - Quản lý kết nối và các truy vấn cơ sở dữ liệu.
import mysql.connector
from mysql.connector import Error
import os

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance._last_config = None
        return cls._instance

    def connect(self, host, user, password, database, port=3306):
        config = (host, user, password, database, port)
        if self.connection and self.connection.is_connected() and self._last_config == config:
            return True

        try:
            # First connect without database to ensure it exists
            temp_conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            temp_conn.close()

            # Now connect to the actual database
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            if self.connection.is_connected():
                self._last_config = config
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            return None
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            # Only commit if NOT a SELECT statement
            if not query.strip().upper().startswith("SELECT"):
                self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            data = cursor.fetchall()
            cursor.close()
            return data
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            data = cursor.fetchone()
            cursor.close()
            return data
        return None

    def run_schema(self, schema_file):
        if not self.connection or not self.connection.is_connected():
            return False
        
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
            
            # Chia schema bằng dấu chấm phẩy và lọc ra các chuỗi trống
            statements = [s.strip() for s in schema.split(';') if s.strip()]
            
            cursor = self.connection.cursor()
            for statement in statements:
                try:
                    cursor.execute(statement)
                except Error as e:
                    print(f"Error executing statement: {e}")
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error running schema: {e}")
            return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

db_manager = DatabaseManager()
