import random
import numpy as np
from database.manager import db_manager
from core.question import Question

class TestSession:
    def __init__(self, user_id, category_id, num_questions=10):
        self.user_id = user_id
        self.category_id = category_id
        self.num_questions = num_questions
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.user_answers = {} # question_id: answer_id

    def generate_test(self):
        all_questions = Question.get_by_category(self.category_id)
        if len(all_questions) > self.num_questions:
            self.questions = random.sample(all_questions, self.num_questions)
        else:
            self.questions = all_questions
            self.num_questions = len(all_questions)
        random.shuffle(self.questions)

    def submit_answer(self, question_id, answer_id):
        self.user_answers[question_id] = answer_id
        
        # Kiểm tra xem có đúng không
        question = next((q for q in self.questions if q.id == question_id), None)
        if question:
            correct_answer = next((a for a in question.answers if a.is_correct), None)
            if correct_answer and correct_answer.id == answer_id:
                self.score += 1

    def finalize_test(self):
        query = "INSERT INTO test_results (user_id, category_id, score, total_questions) VALUES (%s, %s, %s, %s)"
        db_manager.execute_query(query, (self.user_id, self.category_id, self.score, self.num_questions))
        return self.score, self.num_questions

class ResultHistory:
    @staticmethod
    def get_user_results(user_id):
        query = """
            SELECT tr.*, c.name as category_name 
            FROM test_results tr
            LEFT JOIN categories c ON tr.category_id = c.id
            WHERE tr.user_id = %s
            ORDER BY tr.test_date DESC
        """
        return db_manager.fetch_all(query, (user_id,))

    @staticmethod
    def get_all_results():
        query = """
            SELECT tr.*, u.username, c.name as category_name
            FROM test_results tr
            JOIN users u ON tr.user_id = u.id
            LEFT JOIN categories c ON tr.category_id = c.id
            ORDER BY tr.test_date DESC
        """
        return db_manager.fetch_all(query)

class PerformanceAnalyzer:
    @staticmethod
    def calculate_stats(results):
        if not results:
            return None
        
        # Chuyển đổi điểm số thành tỷ lệ phần trăm (0-100)
        scores = np.array([(res['score'] / res['total_questions']) * 100 for res in results])
        
        return {
            'mean': float(np.mean(scores)),
            'median': float(np.median(scores)),
            'std_dev': float(np.std(scores)),
            'max': float(np.max(scores)),
            'min': float(np.min(scores)),
            'count': int(len(scores))
        }
