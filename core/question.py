from database.manager import db_manager

class Category:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @staticmethod
    def get_all():
        query = "SELECT * FROM categories"
        data = db_manager.fetch_all(query)
        return [Category(d['id'], d['name'], d['description']) for d in data]

    @staticmethod
    def add(name, description):
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        db_manager.execute_query(query, (name, description))

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
        query = "SELECT * FROM questions WHERE category_id = %s"
        q_data = db_manager.fetch_all(query, (category_id,))
        
        questions = []
        for q in q_data:
            ans_query = "SELECT * FROM answers WHERE question_id = %s"
            ans_data = db_manager.fetch_all(ans_query, (q['id'],))
            answers = [Answer(a['id'], a['text'], a['is_correct']) for a in ans_data]
            questions.append(Question(q['id'], q['category_id'], q['text'], q['difficulty'], answers))
        return questions

    @staticmethod
    def add_question(category_id, text, difficulty, choices):
        # choices is list of (text, is_correct)
        query = "INSERT INTO questions (category_id, text, difficulty) VALUES (%s, %s, %s)"
        cursor = db_manager.execute_query(query, (category_id, text, difficulty))
        if cursor:
            question_id = cursor.lastrowid
            for text, is_correct in choices:
                ans_query = "INSERT INTO answers (question_id, text, is_correct) VALUES (%s, %s, %s)"
                db_manager.execute_query(ans_query, (question_id, text, is_correct))
            return True
        return False
