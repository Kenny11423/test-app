from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox, 
                             QHBoxLayout, QFrame)
from PySide6.QtCore import Qt
from core.question import Category, Question
from core.test import ResultHistory

class StudentDashboard(QWidget):
    def __init__(self, user, on_start_test, on_logout):
        super().__init__()
        self.user = user
        self.on_start_test = on_start_test
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel(f"Chào mừng, {self.user.username}")
        self.welcome_label.setStyleSheet("font-weight: bold; font-size: 20px; color: #007bff;")
        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.clicked.connect(self.on_logout)
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        self.layout.addLayout(header_layout)

        # Main content
        content_layout = QHBoxLayout()
        
        # Left: Test Selection
        left_panel = QFrame(); left_panel.setObjectName("content_card")
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("### CHỌN BÀI THI"))
        
        # Filters
        filter_layout = QFormLayout()
        self.subject_combo = QComboBox()
        self.grade_combo = QComboBox()
        for i in range(1, 13): self.grade_combo.addItem(f"Lớp {i}", i)
        self.subject_combo.currentIndexChanged.connect(self.refresh_test_list)
        self.grade_combo.currentIndexChanged.connect(self.refresh_test_list)
        filter_layout.addRow("Môn học:", self.subject_combo)
        filter_layout.addRow("Khối lớp:", self.grade_combo)
        left_layout.addLayout(filter_layout)

        self.test_list = QListWidget()
        left_layout.addWidget(self.test_list)

        self.start_btn = QPushButton("Bắt đầu thi")
        self.start_btn.setFixedHeight(40)
        self.start_btn.clicked.connect(self.handle_start_test)
        left_layout.addWidget(self.start_btn)
        content_layout.addWidget(left_panel, 2)

        # Right: History
        right_panel = QFrame(); right_panel.setObjectName("content_card")
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("### KẾT QUẢ CỦA BẠN"))
        self.results_list = QListWidget()
        right_layout.addWidget(self.results_list)
        content_layout.addWidget(right_panel, 3)
        
        self.layout.addLayout(content_layout)
        
        # Initial Load
        self.load_subjects()
        self.refresh_results()

    def load_subjects(self):
        self.subject_combo.blockSignals(True)
        self.subject_combo.clear()
        subjects = Category.get_all()
        for s in subjects:
            self.subject_combo.addItem(s.name, s.id)
        self.subject_combo.blockSignals(False)
        self.refresh_test_list()

    def refresh_test_list(self):
        self.test_list.clear()
        sub_id = self.subject_combo.currentData()
        grade = self.grade_combo.currentData()
        if sub_id is None: return
        
        # Lấy số lượng câu hỏi hiện có của môn này/lớp này
        questions = Question.get_by_category(sub_id, grade)
        if questions:
            item = QListWidgetItem(f"Bài ôn tập: {self.subject_combo.currentText()} - Lớp {grade}")
            item.setData(Qt.UserRole, (sub_id, grade))
            item.setToolTip(f"Tổng số {len(questions)} câu hỏi")
            self.test_list.addItem(item)
        else:
            self.test_list.addItem("Chưa có câu hỏi cho mục này.")

    def refresh_results(self):
        self.results_list.clear()
        results = ResultHistory.get_user_results(self.user.id)
        for res in results:
            text = f"Môn: {res['category_name']} | Lớp {res.get('grade','?')} | Điểm: {res['score']}/{res['total_questions']}"
            self.results_list.addItem(text)

    def handle_start_test(self):
        selected = self.test_list.currentItem()
        if not selected or not selected.data(Qt.UserRole):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một bài thi hợp lệ.")
            return
        
        sub_id, grade = selected.data(Qt.UserRole)
        self.on_start_test(sub_id, grade)

from PySide6.QtWidgets import QFormLayout # Cần import bổ sung
