# File: core/ai_handler.py - Xử lý tạo câu hỏi tự động bằng Gemini AI (Sử dụng SDK mới google-genai).
from google import genai
import json
import re

class AIGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

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
            # Sử dụng SDK mới và model khả dụng ổn định (Gemini Flash Latest)
            response = self.client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            
            text = response.text
            # Trích xuất JSON từ phản hồi
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return None
        except Exception as e:
            print(f"Lỗi Gemini AI (google-genai): {e}")
            return None
