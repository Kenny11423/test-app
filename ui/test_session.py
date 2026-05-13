# File: ui/test_session.py - Giao diện thực hiện bài thi và nộp bài.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QRadioButton, QButtonGroup, QMessageBox, QFrame, QHBoxLayout)
from PySide6.QtCore import QTimer, Qt
from core.test import TestSession

class TestSessionWidget(QWidget):
    def __init__(self, user_id, category_id, grade, category_name, on_test_complete):
        super().__init__()
        self.session = TestSession(user_id, category_id, grade)
        self.session.generate_test()
        self.on_test_complete = on_test_complete
        self.category_name = category_name
        
        self.time_left = self.session.num_questions * 60
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.init_ui()
        self.display_question()
        self.timer.start(1000)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)
        
        # Header với Timer
        header_frame = QFrame()
        header_frame.setObjectName("header_card")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        self.title_label = QLabel(f"Bài thi: {self.category_name} - Lớp {self.session.grade}")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 20px; color: #4a90e2;")
        
        self.timer_label = QLabel(f"⏱ {self.format_time(self.time_left)}")
        self.timer_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #ef4444; background: #fee2e2; padding: 5px 15px; border-radius: 8px;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.timer_label)
        self.main_layout.addWidget(header_frame)

        # Câu hỏi Card
        self.q_card = QFrame()
        self.q_card.setObjectName("question_card")
        self.q_layout = QVBoxLayout(self.q_card)
        self.q_layout.setContentsMargins(30, 30, 30, 30)
        self.q_layout.setSpacing(25)

        self.q_label = QLabel("")
        self.q_label.setWordWrap(True)
        self.q_label.setStyleSheet("font-size: 22px; font-weight: 600; color: #1e293b; line-height: 1.6;")
        self.q_layout.addWidget(self.q_label)

        # Container cho các đáp án
        self.answers_container = QFrame()
        self.answers_layout = QVBoxLayout(self.answers_container)
        self.answers_layout.setSpacing(12)
        
        self.answer_group = QButtonGroup()
        self.answer_buttons = []
        for i in range(4):
            btn = QRadioButton("")
            btn.setStyleSheet("""
                QRadioButton {
                    padding: 15px;
                    font-size: 17px;
                    border: 1px solid #e2e8f0;
                    border-radius: 10px;
                    background: #f8fafc;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                }
                QRadioButton:hover {
                    background: #f1f5f9;
                    border: 1px solid #cbd5e1;
                }
                QRadioButton:checked {
                    background: #eff6ff;
                    border: 2px solid #3b82f6;
                    font-weight: bold;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            self.answer_group.addButton(btn, i)
            self.answers_layout.addWidget(btn)
            self.answer_buttons.append(btn)
        
        self.q_layout.addWidget(self.answers_container)
        self.main_layout.addWidget(self.q_card)

        # Footer với nút điều hướng
        footer_layout = QHBoxLayout()
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("font-size: 16px; font-weight: 500; color: #64748b;")
        
        self.next_btn = QPushButton("Câu tiếp theo")
        self.next_btn.setFixedHeight(50)
        self.next_btn.setMinimumWidth(180)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.handle_next)
        
        footer_layout.addWidget(self.progress_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.next_btn)
        self.main_layout.addLayout(footer_layout)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Thời gian: {self.format_time(self.time_left)}")
        if self.time_left <= 0:
            self.timer.stop()
            QMessageBox.warning(self, "Hết giờ!", "Thời gian làm bài đã kết thúc.")
            self.finish_test()

    def display_question(self):
        if self.session.current_question_index < len(self.session.questions):
            q = self.session.questions[self.session.current_question_index]
            self.q_label.setText(f"Câu {self.session.current_question_index + 1}: {q.text}")
            self.progress_label.setText(f"Tiến độ: {self.session.current_question_index + 1}/{len(self.session.questions)}")
            
            if self.session.current_question_index == len(self.session.questions) - 1:
                self.next_btn.setText("Nộp bài")
            else:
                self.next_btn.setText("Câu tiếp theo")

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
