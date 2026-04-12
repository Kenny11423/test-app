# File: core/ai_handler.py - Xử lý tạo câu hỏi tự động bằng Gemini AI.
import google.generativeai as genai
import json
import re

class AIGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_questions(self, topic, num_questions=5, difficulty='Medium'):
        prompt = f"""
        Bạn là một chuyên gia soạn đề thi. Hãy tạo {num_questions} câu hỏi trắc nghiệm về chủ đề: "{topic}".
        Độ khó: {difficulty}.
        
        Yêu cầu trả về DUY NHẤT một mảng JSON (không có markdown, không có text dư thừa) theo cấu trúc:
        [
          {{
            "text": "Nội dung câu hỏi",
            "choices": [
              {{"text": "Lựa chọn 1", "is_correct": true}},
              {{"text": "Lựa chọn 2", "is_correct": false}},
              {{"text": "Lựa chọn 3", "is_correct": false}},
              {{"text": "Lựa chọn 4", "is_correct": false}}
            ]
          }}
        ]
        Lưu ý: Mỗi câu hỏi phải có đúng 4 lựa chọn và chỉ có 1 lựa chọn đúng.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Trích xuất JSON từ phản hồi (đôi khi AI bao bọc bởi ```json ... ```)
            text = response.text
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return None
        except Exception as e:
            print(f"Lỗi Gemini AI: {e}")
            return None
