from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox)
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
        self.layout = QVBoxLayout()
        
        self.welcome_label = QLabel(f"Chào mừng, {self.user.username}")
        self.layout.addWidget(self.welcome_label)

        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.clicked.connect(self.on_logout)
        self.layout.addWidget(self.logout_btn)

        self.layout.addWidget(QLabel("### Bài thi có sẵn"))
        self.cat_list = QListWidget()
        self.refresh_categories()
        self.layout.addWidget(self.cat_list)

        self.start_btn = QPushButton("Bắt đầu thi")
        self.start_btn.clicked.connect(self.handle_start_test)
        self.layout.addWidget(self.start_btn)

        self.layout.addWidget(QLabel("### Kết quả cũ của bạn"))
        self.results_list = QListWidget()
        self.refresh_results()
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

    def refresh_categories(self):
        self.cat_list.clear()
        categories = Category.get_all()
        for cat in categories:
            item = QListWidgetItem(cat.name)
            item.setData(32, cat.id) # 32 là một vai trò tùy chỉnh
            self.cat_list.addItem(item)

    def refresh_results(self):
        self.results_list.clear()
        results = ResultHistory.get_user_results(self.user.id)
        for res in results:
            text = f"Danh mục: {res['category_name']} | Điểm: {res['score']}/{res['total_questions']} | Ngày: {res['test_date']}"
            self.results_list.addItem(text)

    def handle_start_test(self):
        selected_item = self.cat_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một danh mục bài thi.")
            return
        
        cat_id = selected_item.data(32)
        self.on_start_test(cat_id)
