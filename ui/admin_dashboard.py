from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QTextEdit, 
                             QFormLayout, QHBoxLayout, QListWidget, QSpinBox)
from core.question import Category, Question

class AdminDashboard(QWidget):
    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.welcome_label = QLabel(f"Quản trị viên: {self.user.username}")
        self.layout.addWidget(self.welcome_label)

        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.clicked.connect(self.on_logout)
        self.layout.addWidget(self.logout_btn)

        # Tab or sections
        self.cat_layout = QVBoxLayout()
        self.cat_layout.addWidget(QLabel("### Quản lý Danh mục"))
        self.cat_name_input = QLineEdit()
        self.cat_name_input.setPlaceholderText("Tên Danh mục")
        self.cat_desc_input = QLineEdit()
        self.cat_desc_input.setPlaceholderText("Mô tả")
        self.add_cat_btn = QPushButton("Thêm Danh mục")
        self.add_cat_btn.clicked.connect(self.add_category)
        
        self.cat_layout.addWidget(self.cat_name_input)
        self.cat_layout.addWidget(self.cat_desc_input)
        self.cat_layout.addWidget(self.add_cat_btn)
        self.layout.addLayout(self.cat_layout)

        self.q_layout = QVBoxLayout()
        self.q_layout.addWidget(QLabel("### Quản lý Câu hỏi"))
        
        self.q_cat_combo = QComboBox()
        self.refresh_categories()
        
        self.q_text_input = QTextEdit()
        self.q_text_input.setPlaceholderText("Nội dung câu hỏi")
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem("Dễ", "Easy")
        self.difficulty_combo.addItem("Trung bình", "Medium")
        self.difficulty_combo.addItem("Khó", "Hard")
        
        # Choices
        self.choices_layout = QVBoxLayout()
        self.choice_inputs = []
        for i in range(4):
            h_layout = QHBoxLayout()
            c_input = QLineEdit()
            c_input.setPlaceholderText(f"Lựa chọn {i+1}")
            is_correct_btn = QPushButton("Đúng?")
            is_correct_btn.setCheckable(True)
            h_layout.addWidget(c_input)
            h_layout.addWidget(is_correct_btn)
            self.choices_layout.addLayout(h_layout)
            self.choice_inputs.append((c_input, is_correct_btn))

        self.add_q_btn = QPushButton("Thêm Câu hỏi")
        self.add_q_btn.clicked.connect(self.add_question)

        self.q_layout.addWidget(QLabel("Chọn Danh mục:"))
        self.q_layout.addWidget(self.q_cat_combo)
        self.q_layout.addWidget(QLabel("Nội dung câu hỏi:"))
        self.q_layout.addWidget(self.q_text_input)
        self.q_layout.addWidget(QLabel("Độ khó:"))
        self.q_layout.addWidget(self.difficulty_combo)
        self.q_layout.addLayout(self.choices_layout)
        self.q_layout.addWidget(self.add_q_btn)
        
        self.layout.addLayout(self.q_layout)

        self.res_layout = QVBoxLayout()
        self.res_layout.addWidget(QLabel("### Kết quả học sinh"))
        self.res_list = QListWidget()
        self.refresh_results_btn = QPushButton("Làm mới kết quả")
        self.refresh_results_btn.clicked.connect(self.refresh_results)
        self.export_res_btn = QPushButton("Xuất ra CSV")
        self.export_res_btn.clicked.connect(self.export_to_csv)
        
        self.res_layout.addWidget(self.res_list)
        self.res_layout.addWidget(self.refresh_results_btn)
        self.res_layout.addWidget(self.export_res_btn)
        self.layout.addLayout(self.res_layout)

        self.setLayout(self.layout)
        self.refresh_results()

    def refresh_results(self):
        from core.test import ResultHistory
        self.res_list.clear()
        results = ResultHistory.get_all_results()
        for res in results:
            text = f"Người dùng: {res['username']} | Danh mục: {res['category_name']} | Điểm: {res['score']}/{res['total_questions']} | Ngày: {res['test_date']}"
            self.res_list.addItem(text)

    def export_to_csv(self):
        import csv
        from core.test import ResultHistory
        results = ResultHistory.get_all_results()
        if not results:
            return
        
        with open('all_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        QMessageBox.information(self, "Thành công", "Đã xuất kết quả ra file all_results.csv")

    def refresh_categories(self):
        self.q_cat_combo.clear()
        categories = Category.get_all()
        for cat in categories:
            self.q_cat_combo.addItem(cat.name, cat.id)

    def add_category(self):
        name = self.cat_name_input.text()
        desc = self.cat_desc_input.text()
        if not name:
            return
        Category.add(name, desc)
        QMessageBox.information(self, "Thành công", "Đã thêm danh mục!")
        self.refresh_categories()

    def add_question(self):
        cat_id = self.q_cat_combo.currentData()
        text = self.q_text_input.toPlainText()
        diff = self.difficulty_combo.currentData() # Use data for internal value
        
        choices = []
        for c_input, is_correct_btn in self.choice_inputs:
            c_text = c_input.text()
            if not c_text: continue
            choices.append((c_text, is_correct_btn.isChecked()))
        
        if not text or not choices:
            QMessageBox.warning(self, "Lỗi", "Yêu cầu nhập nội dung câu hỏi và các lựa chọn.")
            return

        if Question.add_question(cat_id, text, diff, choices):
            QMessageBox.information(self, "Thành công", "Đã thêm câu hỏi!")
            self.q_text_input.clear()
            for c_input, is_correct_btn in self.choice_inputs:
                c_input.clear()
                is_correct_btn.setChecked(False)
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể thêm câu hỏi.")
