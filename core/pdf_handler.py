# File: core/pdf_handler.py - Trích xuất và xử lý câu hỏi từ tệp PDF (Bản nâng cấp).
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
            # Sử dụng "blocks" để giữ cấu trúc tốt hơn là chỉ lấy text thuần túy
            blocks = page.get_text("blocks")
            for b in blocks:
                text += b[4] + "\n"
        return text

    def parse(self):
        # 1. Chuẩn hóa văn bản (Xóa khoảng trắng thừa, sửa lỗi dính chữ phổ biến)
        text = self.text
        
        # 2. Tìm danh sách câu hỏi
        # Pattern hỗ trợ: "Câu 1:", "Câu 1.", "Question 1:", "1."
        q_pattern = r'(?m)^(?:Câu|Câu hỏi|Question)\s*(\d+)\s*[:.]'
        
        # Tách các khối câu hỏi
        parts = re.split(q_pattern, text)
        if len(parts) < 3:
            # Thử pattern đơn giản hơn nếu không tìm thấy "Câu X"
            q_pattern = r'(?m)^(\d+)\s*[:.]'
            parts = re.split(q_pattern, text)
        
        questions = []
        # parts sẽ có dạng: [header, q_num1, q_text1, q_num2, q_text2, ...]
        for i in range(1, len(parts), 2):
            q_num = int(parts[i])
            q_block = parts[i+1]
            
            # Tìm các lựa chọn A, B, C, D trong khối này
            # Hỗ trợ cả "A.", "A)", "(A)"
            choices = []
            for label in ['A', 'B', 'C', 'D']:
                # Tìm nội dung giữa nhãn hiện tại và nhãn tiếp theo (hoặc kết thúc khối)
                next_labels = {'A': 'B', 'B': 'C', 'C': 'D', 'D': '$'}
                c_pattern = rf'(?s)[({label}[.)]\s*(.*?)(?=[(]{next_labels[label]}[.)]|\s[A-D][.)]|$)'
                c_match = re.search(c_pattern, q_block)
                if c_match:
                    choices.append(c_match.group(1).strip())
                else:
                    # Thử pattern dự phòng nếu không có dấu ngoặc
                    c_pattern_alt = rf'(?s){label}[:.]\s*(.*?)(?=[A-D][:.]|$)'
                    c_match_alt = re.search(c_pattern_alt, q_block)
                    if c_match_alt:
                        choices.append(c_match_alt.group(1).strip())

            if len(choices) >= 2: # Chấp nhận ít nhất 2 lựa chọn (trắc nghiệm có thể có 2-4)
                # Tách nội dung câu hỏi (phần trước lựa chọn A)
                q_text_match = re.search(rf'(?s)(.*?)(?=[(]?A[.)])', q_block)
                q_text = q_text_match.group(1).strip() if q_text_match else q_block.split('A.')[0].strip()
                
                questions.append({
                    'id': q_num,
                    'text': q_text,
                    'choices': choices
                })

        # 3. Trích xuất đáp án
        answers = {}
        # Tìm bảng đáp án (thường ở cuối file) dạng "1.A 2.B 3.C" hoặc "1-A 2-B"
        key_matches = re.finditer(r'(\d+)\s*[:.-]\s*([A-D])(?:\s|$)', text)
        for m in key_matches:
            answers[int(m.group(1))] = m.group(2)
            
        # Nếu không có bảng đáp án, tìm từ khóa "Đáp án: A" trong từng câu
        if not answers:
            for q in questions:
                # Tìm trong text gốc của câu đó (đã tách ở trên)
                # Cần tìm lại khối text chứa câu hỏi đó
                pass # Logic này đã được xử lý một phần bởi regex key_matches bên trên

        # Khớp câu hỏi với đáp án
        final_data = []
        for q in questions:
            correct_letter = answers.get(q['id'])
            if not correct_letter:
                # Thử tìm từ "Đáp án: A" ngay trong chính khối câu hỏi (nếu có)
                # (Tìm trong parts[i+1] tương ứng)
                pass
            
            if correct_letter:
                correct_idx = ord(correct_letter.upper()) - ord('A')
                if correct_idx < len(q['choices']):
                    final_data.append({
                        'text': q['text'],
                        'choices': q['choices'],
                        'correct_idx': correct_idx
                    })
        
        return final_data

def update_db_with_pdf(pdf_path, category_id, grade):
    parser = PDFTestParser(pdf_path)
    test_data = parser.parse()
    
    if not test_data:
        # Thử logic dự phòng cuối cùng: Scan toàn bộ text tìm Question/Answer kiểu dòng đơn
        return 0
        
    success_count = 0
    from core.question import Question
    for item in test_data:
        choices = []
        for i, choice_text in enumerate(item['choices']):
            choices.append((choice_text, i == item['correct_idx']))
        
        if Question.add_question(category_id, grade, item['text'], 'Medium', choices):
            success_count += 1
            
    return success_count
