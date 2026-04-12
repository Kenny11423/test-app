# File: core/question.py - Định nghĩa cấu trúc và logic cho các câu hỏi.
from database.manager import db_manager

class Category:
    _cache = None

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @staticmethod
    def get_all(force_refresh=False):
        if Category._cache is not None and not force_refresh:
            return Category._cache
            
        query = "SELECT * FROM categories"
        data = db_manager.fetch_all(query)
        Category._cache = [Category(d['id'], d['name'], d['description']) for d in data]
        return Category._cache

    @staticmethod
    def add(name, description):
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        cursor = db_manager.execute_query(query, (name, description))
        if cursor and hasattr(cursor, '_pool_conn'):
            cursor._pool_conn.close()
        Category._cache = None

    @staticmethod
    def update(cat_id, name, description):
        query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
        cursor = db_manager.execute_query(query, (name, description, cat_id))
        if cursor and hasattr(cursor, '_pool_conn'):
            cursor._pool_conn.close()
        Category._cache = None
        return True

class Answer:
    def __init__(self, id, text, is_correct):
        self.id = id
        self.text = text
        self.is_correct = is_correct

class Question:
    def __init__(self, id, category_id, grade, text, difficulty, answers=None):
        self.id = id
        self.category_id = category_id
        self.grade = grade
        self.text = text
        self.difficulty = difficulty
        self.answers = answers or []

    @staticmethod
    def get_by_category(category_id, grade=None):
        # Sử dụng JOIN để lấy toàn bộ câu hỏi và đáp án
        query = """
            SELECT q.id as q_id, q.category_id, q.grade, q.text as q_text, q.difficulty,
                   a.id as a_id, a.text as a_text, a.is_correct
            FROM questions q
            LEFT JOIN answers a ON q.id = a.question_id
            WHERE q.category_id = %s
        """
        params = [category_id]
        if grade is not None:
            query += " AND q.grade = %s"
            params.append(grade)
            
        query += " ORDER BY q.id"
        data = db_manager.fetch_all(query, tuple(params))
        
        questions_dict = {}
        for row in data:
            q_id = row['q_id']
            if q_id not in questions_dict:
                questions_dict[q_id] = Question(
                    q_id, row['category_id'], row['grade'], row['q_text'], row['difficulty']
                )
            
            if row['a_id']:
                ans = Answer(row['a_id'], row['a_text'], row['is_correct'])
                questions_dict[q_id].answers.append(ans)
                
        return list(questions_dict.values())

    @staticmethod
    def add_question(category_id, grade, text, difficulty, choices):
        # choices là danh sách các (nội dung, là_đáp_án_đúng)
        query = "INSERT INTO questions (category_id, grade, text, difficulty) VALUES (%s, %s, %s, %s)"
        cursor = db_manager.execute_query(query, (category_id, grade, text, difficulty))
        if cursor:
            question_id = cursor.lastrowid
            if hasattr(cursor, '_pool_conn'):
                cursor._pool_conn.close() # Đóng kết nối của INSERT question
            
            for a_text, is_correct in choices:
                ans_query = "INSERT INTO answers (question_id, text, is_correct) VALUES (%s, %s, %s)"
                ans_cursor = db_manager.execute_query(ans_query, (question_id, a_text, is_correct))
                if ans_cursor and hasattr(ans_cursor, '_pool_conn'):
                    ans_cursor._pool_conn.close()
            return True
        return False

    @staticmethod
    def delete(question_id):
        query = "DELETE FROM questions WHERE id = %s"
        cursor = db_manager.execute_query(query, (question_id,))
        if cursor and hasattr(cursor, '_pool_conn'):
            cursor._pool_conn.close()
        return True

    @staticmethod
    def update_question(question_id, category_id, grade, text, difficulty, choices):
        query = "UPDATE questions SET category_id = %s, grade = %s, text = %s, difficulty = %s WHERE id = %s"
        cursor = db_manager.execute_query(query, (category_id, grade, text, difficulty, question_id))
        if cursor and hasattr(cursor, '_pool_conn'):
            cursor._pool_conn.close()
        
        # Xóa đáp án cũ và thêm mới
        cursor = db_manager.execute_query("DELETE FROM answers WHERE question_id = %s", (question_id,))
        if cursor and hasattr(cursor, '_pool_conn'):
            cursor._pool_conn.close()

        for a_text, is_correct in choices:
            ans_query = "INSERT INTO answers (question_id, text, is_correct) VALUES (%s, %s, %s)"
            cursor = db_manager.execute_query(ans_query, (question_id, a_text, is_correct))
            if cursor and hasattr(cursor, '_pool_conn'):
                cursor._pool_conn.close()
        return True
