# File: ui/test_session.py - Giao diện thực hiện bài thi và nộp bài.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QRadioButton, QButtonGroup, QMessageBox)
from PySide6.QtCore import QTimer
from core.test import TestSession

class TestSessionWidget(QWidget):
    def __init__(self, user_id, category_id, on_test_complete):
        super().__init__()
        self.session = TestSession(user_id, category_id)
        self.session.generate_test()
        self.on_test_complete = on_test_complete
        
        self.time_left = self.session.num_questions * 60 # 1 minute per question
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.init_ui()
        self.display_question()
        self.timer.start(1000)

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.timer_label = QLabel(f"Thời gian còn lại: {self.format_time(self.time_left)}")
        self.layout.addWidget(self.timer_label)

        self.q_label = QLabel("")
        self.q_label.setWordWrap(True)
        self.layout.addWidget(self.q_label)

        self.answer_group = QButtonGroup()
        self.answer_buttons = []
        for i in range(4):
            btn = QRadioButton("")
            self.answer_group.addButton(btn, i)
            self.layout.addWidget(btn)
            self.answer_buttons.append(btn)

        self.next_btn = QPushButton("Câu tiếp theo")
        self.next_btn.clicked.connect(self.handle_next)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Thời gian còn lại: {self.format_time(self.time_left)}")
        if self.time_left <= 0:
            self.timer.stop()
            QMessageBox.warning(self, "Hết giờ!", "Thời gian làm bài đã kết thúc.")
            self.finish_test()

    def display_question(self):
        if self.session.current_question_index < len(self.session.questions):
            q = self.session.questions[self.session.current_question_index]
            self.q_label.setText(f"Câu {self.session.current_question_index + 1}: {q.text}")
            
            # Đặt lại các nút
            self.answer_group.setExclusive(False)
            for btn in self.answer_buttons:
                btn.setChecked(False)
                btn.hide()
            self.answer_group.setExclusive(True)

            for i, ans in enumerate(q.answers):
                if i < len(self.answer_buttons):
                    self.answer_buttons[i].setText(ans.text)
                    self.answer_buttons[i].show()
                    self.answer_group.setId(self.answer_buttons[i], ans.id)
        else:
            self.finish_test()

    def handle_next(self):
        selected_id = self.answer_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một câu trả lời.")
            return

        current_q = self.session.questions[self.session.current_question_index]
        self.session.submit_answer(current_q.id, selected_id)
        
        self.session.current_question_index += 1
        self.display_question()

    def finish_test(self):
        self.timer.stop()
        score, total = self.session.finalize_test()
        QMessageBox.information(self, "Hoàn thành bài thi", f"Bạn đã đạt {score} trên tổng số {total} điểm!")
        self.on_test_complete()
