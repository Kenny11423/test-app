from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QTextEdit, 
                             QFormLayout, QHBoxLayout, QListWidget, QSpinBox,
                             QFileDialog, QTabWidget, QListWidgetItem)
from core.question import Category, Question
from PySide6.QtCore import Qt

class AdminDashboard(QWidget):
    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel(f"Quản trị viên: {self.user.username}")
        self.welcome_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.clicked.connect(self.on_logout)
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        self.main_layout.addLayout(header_layout)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Categories & Add Questions
        self.tab1 = QWidget()
        self.setup_tab1()
        self.tabs.addTab(self.tab1, "Thêm Câu hỏi")

        # Tab 2: Manage Existing Questions
        self.tab2 = QWidget()
        self.setup_tab2()
        self.tabs.addTab(self.tab2, "Quản lý Đề thi")

        # Tab 3: Results
        self.tab3 = QWidget()
        self.setup_tab3()
        self.tabs.addTab(self.tab3, "Kết quả")

        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)
        
        # Initial refreshes
        self.refresh_categories()
        self.refresh_results()
        self.refresh_manage_questions()

    def setup_tab1(self):
        layout = QVBoxLayout(self.tab1)
        
        # Categories section
        cat_group = QVBoxLayout()
        cat_group.addWidget(QLabel("### Quản lý Danh mục (Lớp học)"))
        self.cat_name_input = QLineEdit()
        self.cat_name_input.setPlaceholderText("Tên Danh mục (VD: Toán 12)")
        self.cat_desc_input = QLineEdit()
        self.cat_desc_input.setPlaceholderText("Mô tả")
        self.add_cat_btn = QPushButton("Thêm Danh mục")
        self.add_cat_btn.clicked.connect(self.add_category)
        
        cat_group.addWidget(self.cat_name_input)
        cat_group.addWidget(self.cat_desc_input)
        cat_group.addWidget(self.add_cat_btn)
        layout.addLayout(cat_group)

        layout.addSpacing(20)

        # Phần Thêm Câu hỏi
        q_group = QVBoxLayout()
        q_group.addWidget(QLabel("### Thêm Câu hỏi mới"))
        
        self.q_cat_combo = QComboBox()
        
        self.q_text_input = QTextEdit()
        self.q_text_input.setPlaceholderText("Nội dung câu hỏi")
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem("Dễ", "Easy")
        self.difficulty_combo.addItem("Trung bình", "Medium")
        self.difficulty_combo.addItem("Khó", "Hard")
        
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

        h_btn_layout = QHBoxLayout()
        self.add_q_btn = QPushButton("Thêm Câu hỏi")
        self.add_q_btn.clicked.connect(self.add_question)
        self.import_pdf_btn = QPushButton("Nhập từ PDF")
        self.import_pdf_btn.clicked.connect(self.import_from_pdf)
        h_btn_layout.addWidget(self.add_q_btn)
        h_btn_layout.addWidget(self.import_pdf_btn)

        q_group.addWidget(QLabel("Chọn Danh mục:"))
        q_group.addWidget(self.q_cat_combo)
        q_group.addWidget(QLabel("Nội dung câu hỏi:"))
        q_group.addWidget(self.q_text_input)
        q_group.addWidget(QLabel("Độ khó:"))
        q_group.addWidget(self.difficulty_combo)
        q_group.addLayout(self.choices_layout)
        q_group.addLayout(h_btn_layout)
        layout.addLayout(q_group)

    def setup_tab2(self):
        layout = QVBoxLayout(self.tab2)
        layout.addWidget(QLabel("### Danh sách Câu hỏi hiện có"))
        
        self.manage_cat_combo = QComboBox()
        self.manage_cat_combo.currentIndexChanged.connect(self.refresh_manage_questions)
        layout.addWidget(QLabel("Lọc theo danh mục:"))
        layout.addWidget(self.manage_cat_combo)
        
        self.q_list = QListWidget()
        layout.addWidget(self.q_list)
        
        h_layout = QHBoxLayout()
        self.delete_q_btn = QPushButton("Xóa Câu hỏi")
        self.delete_q_btn.setStyleSheet("background-color: #f44336; color: white;")
        self.delete_q_btn.clicked.connect(self.delete_question)
        self.refresh_q_btn = QPushButton("Làm mới danh sách")
        self.refresh_q_btn.clicked.connect(self.refresh_manage_questions)
        
        h_layout.addWidget(self.delete_q_btn)
        h_layout.addWidget(self.refresh_q_btn)
        layout.addLayout(h_layout)

    def setup_tab3(self):
        layout = QVBoxLayout(self.tab3)
        layout.addWidget(QLabel("### Kết quả học sinh"))
        
        # Thống kê nhanh
        self.stats_label = QLabel("Đang tải thống kê...")
        self.stats_label.setStyleSheet("background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #2196f3;")
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)

        self.res_list = QListWidget()
        self.refresh_results_btn = QPushButton("Làm mới kết quả")
        self.refresh_results_btn.clicked.connect(self.refresh_results)
        self.export_res_btn = QPushButton("Xuất ra CSV")
        self.export_res_btn.clicked.connect(self.export_to_csv)
        
        layout.addWidget(self.res_list)
        layout.addWidget(self.refresh_results_btn)
        layout.addWidget(self.export_res_btn)

    def refresh_manage_questions(self):
        self.q_list.clear()
        cat_id = self.manage_cat_combo.currentData()
        if cat_id is None: return
        
        questions = Question.get_by_category(cat_id)
        for q in questions:
            item = QListWidgetItem(f"ID: {q.id} | {q.text[:60]}...")
            item.setData(Qt.UserRole, q.id)
            self.q_list.addItem(item)

    def delete_question(self):
        selected_item = self.q_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn câu hỏi cần xóa.")
            return
        
        q_id = selected_item.data(Qt.UserRole)
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa câu hỏi ID {q_id}?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            if Question.delete(q_id):
                QMessageBox.information(self, "Thành công", "Đã xóa câu hỏi.")
                self.refresh_manage_questions()

    def refresh_results(self):
        from core.test import ResultHistory, PerformanceAnalyzer
        self.res_list.clear()
        results = ResultHistory.get_all_results()
        
        # Cập nhật thống kê bằng NumPy
        stats = PerformanceAnalyzer.calculate_stats(results)
        if stats:
            self.stats_label.setText(
                f"📊 <b>Thống kê nhanh:</b><br>"
                f"Tổng số bài thi: {stats['count']} | "
                f"Trung bình: {stats['mean']:.1f}% | "
                f"Trung vị: {stats['median']:.1f}% | "
                f"Độ lệch chuẩn: {stats['std_dev']:.1f}<br>"
                f"Cao nhất: {stats['max']:.1f}% | Thấp nhất: {stats['min']:.1f}%"
            )
        else:
            self.stats_label.setText("Chưa có dữ liệu thống kê.")

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
        self.manage_cat_combo.clear()
        categories = Category.get_all()
        for cat in categories:
            self.q_cat_combo.addItem(cat.name, cat.id)
            self.manage_cat_combo.addItem(cat.name, cat.id)

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
        diff = self.difficulty_combo.currentData()
        
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
            self.refresh_manage_questions()
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể thêm câu hỏi.")

    def import_from_pdf(self):
        cat_id = self.q_cat_combo.currentData()
        if not cat_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hoặc tạo danh mục trước.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file PDF Test", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                from core.pdf_handler import update_db_with_pdf
                count = update_db_with_pdf(file_path, cat_id)
                if count > 0:
                    QMessageBox.information(self, "Thành công", f"Đã nhập thành công {count} câu hỏi từ PDF!")
                    self.refresh_manage_questions()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không tìm thấy câu hỏi hoặc đáp án hợp lệ trong PDF.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Có lỗi khi xử lý PDF: {e}")

