import bcrypt
from database.manager import db_manager

class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

class UserManager:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        # Xử lý các trường hợp hashed_password có thể là str hoặc bytes/bytearray
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        elif isinstance(hashed_password, (bytearray, bytes)):
            hashed_password = bytes(hashed_password)
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    @staticmethod
    def register_user(username, password, role='Student'):
        hashed_password = UserManager.hash_password(password)
        query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        cursor = db_manager.execute_query(query, (username, hashed_password, role))
        if cursor:
            return True
        return False

    @staticmethod
    def login_user(username, password):
        query = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
        user_data = db_manager.fetch_one(query, (username,))
        
        if user_data and UserManager.verify_password(password, user_data['password_hash']):
            return User(user_data['id'], user_data['username'], user_data['role'])
        return None
