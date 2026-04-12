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
        # Đây là một nhiệm vụ phức tạp vì tệp PDF có nhiều bài kiểm tra và đáp án.
        # Chúng tôi sẽ tìm kiếm các Câu hỏi và Đáp án tương ứng của chúng.
        
        # 1. Trích xuất tất cả các câu hỏi và các lựa chọn của chúng
        # Mẫu: Question \d+[.:] (.*?) A\. (.*?) B\. (.*?) C\. (.*?) D\. (.*?)
        # Lưu ý: Các lựa chọn có thể được phân tách bằng dòng mới hoặc khoảng trắng.
        
        # Hãy thử chia văn bản thành các khối bắt đầu bằng "Question"
        question_blocks = re.split(r'Question \d+[.(]?[A-Z]{0,3}[)]?[.:]', self.text)
        # Khối đầu tiên thường là văn bản tiêu đề
        header = question_blocks[0]
        question_blocks = question_blocks[1:]
        
        questions = []
        for i, block in enumerate(question_blocks):
            # Thử tìm các tùy chọn A, B, C, D
            # Chúng tôi sử dụng khớp tham lam cho văn bản câu hỏi cho đến khi gặp "A."
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

        # 2. Trích xuất Đáp án
        # Mẫu: Question \d+[.:]?\s*Đáp án[:\s]*([A-D])
        answers = {}
        ans_matches = re.finditer(r'Question (\d+)[^A-D]*Đáp án[:\s]*([A-D])', self.text)
        for m in ans_matches:
            q_num = int(m.group(1))
            ans_letter = m.group(2)
            answers[q_num] = ans_letter

        # Đồng thời tìm kiếm "Câu \d+: Đáp án [A-D]"
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
                # Ánh xạ A->0, B->1, C->2, D->3
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
    
    success_count = 0
    for item in test_data:
        choices = []
        for i, choice_text in enumerate(item['choices']):
            choices.append((choice_text, i == item['correct_idx']))
        
        # Hiện tại giả định độ khó là 'Medium'
        from core.question import Question
        if Question.add_question(category_id, item['text'], 'Medium', choices):
            success_count += 1
            
    return success_count

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        pdf = sys.argv[1]
        cat_id = int(sys.argv[2])
        count = update_db_with_pdf(pdf, cat_id)
        print(f"Successfully added {count} questions.")
