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
        db_manager.execute_query(query, (name, description))
        Category._cache = None

    @staticmethod
    def update(cat_id, name, description):
        query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
        db_manager.execute_query(query, (name, description, cat_id))
        Category._cache = None
        return True

class Answer:
    def __init__(self, id, text, is_correct):
        self.id = id
        self.text = text
        self.is_correct = is_correct

class Question:
    def __init__(self, id, category_id, text, difficulty, answers=None):
        self.id = id
        self.category_id = category_id
        self.text = text
        self.difficulty = difficulty
        self.answers = answers or []

    @staticmethod
    def get_by_category(category_id):
        # Sử dụng JOIN để lấy toàn bộ câu hỏi và đáp án trong 1 lần truy vấn duy nhất
        query = """
            SELECT q.id as q_id, q.category_id, q.text as q_text, q.difficulty,
                   a.id as a_id, a.text as a_text, a.is_correct
            FROM questions q
            LEFT JOIN answers a ON q.id = a.question_id
            WHERE q.category_id = %s
            ORDER BY q.id
        """
        data = db_manager.fetch_all(query, (category_id,))
        
        questions_dict = {}
        for row in data:
            q_id = row['q_id']
            if q_id not in questions_dict:
                questions_dict[q_id] = Question(
                    q_id, row['category_id'], row['q_text'], row['difficulty']
                )
            
            if row['a_id']:
                ans = Answer(row['a_id'], row['a_text'], row['is_correct'])
                questions_dict[q_id].answers.append(ans)
                
        return list(questions_dict.values())

    @staticmethod
    def add_question(category_id, text, difficulty, choices):
        # choices là danh sách các (nội dung, là_đáp_án_đúng)
        query = "INSERT INTO questions (category_id, text, difficulty) VALUES (%s, %s, %s)"
        cursor = db_manager.execute_query(query, (category_id, text, difficulty))
        if cursor:
            question_id = cursor.lastrowid
            for text, is_correct in choices:
                ans_query = "INSERT INTO answers (question_id, text, is_correct) VALUES (%s, %s, %s)"
                db_manager.execute_query(ans_query, (question_id, text, is_correct))
            return True
        return False

    @staticmethod
    def delete(question_id):
        query = "DELETE FROM questions WHERE id = %s"
        db_manager.execute_query(query, (question_id,))
        return True

    @staticmethod
    def update_question(question_id, category_id, text, difficulty, choices):
        # choices là danh sách các (nội dung_đáp_án, là_đúng)
        query = "UPDATE questions SET category_id = %s, text = %s, difficulty = %s WHERE id = %s"
        db_manager.execute_query(query, (category_id, text, difficulty, question_id))
        
        # Xóa đáp án cũ và thêm mới (đơn giản nhất)
        db_manager.execute_query("DELETE FROM answers WHERE question_id = %s", (question_id,))
        for a_text, is_correct in choices:
            ans_query = "INSERT INTO answers (question_id, text, is_correct) VALUES (%s, %s, %s)"
            db_manager.execute_query(ans_query, (question_id, a_text, is_correct))
        return True
