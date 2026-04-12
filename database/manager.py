# File: database/manager.py - Quản lý kết nối và các truy vấn cơ sở dữ liệu.
import mysql.connector
from mysql.connector import Error, pooling
import os

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.pool = None
            cls._instance._last_config = None
        return cls._instance

    def connect(self, host, user, password, database, port=3306):
        config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port
        }
        
        # Nếu cấu hình không đổi và pool đã có, không cần tạo lại
        config_tuple = (host, user, password, database, port)
        if self.pool and self._last_config == config_tuple:
            return True

        try:
            # Đảm bảo database tồn tại
            temp_conn = mysql.connector.connect(host=host, user=user, password=password, port=port)
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            temp_conn.close()

            # Tạo Connection Pool
            self.pool = pooling.MySQLConnectionPool(
                pool_name="test_prep_pool",
                pool_size=5, # Cho phép tối đa 5 kết nối đồng thời
                **config
            )
            self._last_config = config_tuple
            return True
        except Error as e:
            print(f"Error connecting to MySQL Pool: {e}")
            return False

    def get_connection(self):
        if not self.pool:
            return None
        return self.pool.get_connection()

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if not conn: return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if not query.strip().upper().startswith("SELECT"):
                conn.commit()
            # Vì logic cũ dùng cursor sau khi gọi hàm này, ta phải giữ conn mở.
            # Nhưng để tránh rò rỉ, ta nên sửa các hàm gọi.
            # Tạm thời: Gắn conn vào cursor để có thể đóng sau.
            cursor._pool_conn = conn 
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            if conn: conn.close()
            return None

    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetch_all: {e}")
            return []
        finally:
            cursor.close()
            conn.close() # Trả kết nối về pool

    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetch_one: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def run_schema(self, schema_file):
        conn = self.get_connection()
        if not conn: return False
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
            statements = [s.strip() for s in schema.split(';') if s.strip()]
            cursor = conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

db_manager = DatabaseManager()
