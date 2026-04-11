# File: core/pdf_handler.py - Trích xuất và xử lý câu hỏi từ tệp PDF.
import fitz
import re
from database.manager import db_manager

class PDFTestParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self._extract_text()

    def _extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def parse(self):
        # 1. Trích xuất tất cả các câu hỏi và các lựa chọn của chúng
        # Các mẫu cho các định dạng câu hỏi khác nhau
        question_blocks = re.split(r'Question \d+[.(]?[A-Z]{0,3}[)]?[.:]', self.text)
        question_blocks = question_blocks[1:]
        
        questions = []
        for i, block in enumerate(question_blocks):
            # Thử tìm các tùy chọn A, B, C, D
            match = re.search(r'(?s)(.*?)\s*A\.\s*(.*?)\s*B\.\s*(.*?)\s*C\.\s*(.*?)\s*D\.\s*(.*?)(?=\n|$|Question|\d+\.)', block)
            if match:
                q_text = match.group(1).strip()
                choice_a = match.group(2).strip()
                choice_b = match.group(3).strip()
                choice_c = match.group(4).strip()
                choice_d = match.group(5).strip()
                
                questions.append({
                    'id': i + 1,
                    'text': q_text,
                    'choices': [choice_a, choice_b, choice_c, choice_d]
                })

        # 2. Trích xuất đáp án
        answers = {}
        # Định dạng: Question 1: Đáp án A
        ans_matches = re.finditer(r'Question (\d+)[^A-D]*Đáp án[:\s]*([A-D])', self.text)
        for m in ans_matches:
            q_num = int(m.group(1))
            ans_letter = m.group(2)
            answers[q_num] = ans_letter

        # Định dạng: Câu 1: Đáp án A
        ans_matches_cau = re.finditer(r'Câu (\d+)[:\s]*Đáp án[:\s]*([A-D])', self.text)
        for m in ans_matches_cau:
            q_num = int(m.group(1))
            ans_letter = m.group(2)
            answers[q_num] = ans_letter
            
        # Khớp câu hỏi với đáp án
        final_data = []
        for q in questions:
            if q['id'] in answers:
                correct_letter = answers[q['id']]
                correct_idx = ord(correct_letter) - ord('A')
                final_data.append({
                    'text': q['text'],
                    'choices': q['choices'],
                    'correct_idx': correct_idx
                })
        
        return final_data

def update_db_with_pdf(pdf_path, category_id):
    parser = PDFTestParser(pdf_path)
    test_data = parser.parse()
    
    if not test_data:
        return 0
        
    success_count = 0
    from core.question import Question
    for item in test_data:
        choices = []
        for i, choice_text in enumerate(item['choices']):
            choices.append((choice_text, i == item['correct_idx']))
        
        if Question.add_question(category_id, item['text'], 'Medium', choices):
            success_count += 1
            
    return success_count
