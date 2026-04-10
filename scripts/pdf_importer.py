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
        # This is a complex task because the PDF has multiple tests and keys.
        # We will look for Questions and their corresponding Answers.
        
        # 1. Extract all questions and their choices
        # Pattern: Question \d+[.:] (.*?) A\. (.*?) B\. (.*?) C\. (.*?) D\. (.*?)
        # Note: Choices might be separated by newlines or spaces.
        
        # Let's try to split the text into blocks starting with "Question"
        question_blocks = re.split(r'Question \d+[.(]?[A-Z]{0,3}[)]?[.:]', self.text)
        # The first block is usually header text
        header = question_blocks[0]
        question_blocks = question_blocks[1:]
        
        questions = []
        for i, block in enumerate(question_blocks):
            # Try to find options A, B, C, D
            # We use a greedy match for the question text until we hit "A."
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

        # 2. Extract Answer Keys
        # Pattern: Question \d+[.:]?\s*Đáp án[:\s]*([A-D])
        answers = {}
        ans_matches = re.finditer(r'Question (\d+)[^A-D]*Đáp án[:\s]*([A-D])', self.text)
        for m in ans_matches:
            q_num = int(m.group(1))
            ans_letter = m.group(2)
            answers[q_num] = ans_letter

        # Also search for "Câu \d+: Đáp án [A-D]"
        ans_matches_cau = re.finditer(r'Câu (\d+)[:\s]*Đáp án[:\s]*([A-D])', self.text)
        for m in ans_matches_cau:
            q_num = int(m.group(1))
            ans_letter = m.group(2)
            answers[q_num] = ans_letter
            
        # Match questions with answers
        final_data = []
        for q in questions:
            if q['id'] in answers:
                correct_letter = answers[q['id']]
                # Map A->0, B->1, C->2, D->3
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
        
        # Assuming difficulty is 'Medium' for now
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
