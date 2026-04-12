# File: ui/student_dashboard.py - Giao diện cho học sinh.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox, 
                             QHBoxLayout, QFrame)
from PySide6.QtCore import Qt
from core.question import Category
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
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.on_logout)
        
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        self.layout.addLayout(header_layout)

        # Main content area
        content_layout = QHBoxLayout()
        
        # Left side: Test selection
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel.setObjectName("content_card")
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("### BÀI THI CÓ SẴN"))
        self.cat_list = QListWidget()
        self.refresh_categories()
        left_layout.addWidget(self.cat_list)

        self.start_btn = QPushButton("Bắt đầu thi")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.handle_start_test)
        left_layout.addWidget(self.start_btn)
        
        content_layout.addWidget(left_panel, 2)

        # Right side: History
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_panel.setObjectName("content_card")
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("### LỊCH SỬ KẾT QUẢ"))
        self.results_list = QListWidget()
        self.refresh_results()
        right_layout.addWidget(self.results_list)
        
        content_layout.addWidget(right_panel, 3)
        
        self.layout.addLayout(content_layout)

    def refresh_categories(self):
        self.cat_list.clear()
        categories = Category.get_all()
        for cat in categories:
            item = QListWidgetItem(cat.name)
            item.setData(Qt.UserRole, cat.id)
            self.cat_list.addItem(item)

    def refresh_results(self):
        self.results_list.clear()
        results = ResultHistory.get_user_results(self.user.id)
        for res in results:
            text = f"Đề: {res['category_name']}\nĐiểm: {res['score']}/{res['total_questions']} | Ngày: {res['test_date']}"
            self.results_list.addItem(text)

    def handle_start_test(self):
        selected_item = self.cat_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một danh mục bài thi.")
            return
        
        cat_id = selected_item.data(Qt.UserRole)
        self.on_start_test(cat_id)
