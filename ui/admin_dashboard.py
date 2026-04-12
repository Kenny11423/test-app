from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QTextEdit, 
                             QFormLayout, QHBoxLayout, QListWidget, QSpinBox,
                             QFileDialog, QTabWidget, QListWidgetItem, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView, QDialog)
from core.question import Category, Question
from PySide6.QtCore import Qt, QThread, Signal

class DataLoader(QThread):
    data_loaded = Signal(object) # Dùng object để hỗ trợ cả list, dict hoặc tuple
    
    def __init__(self, fetch_func, *args):
        super().__init__()
        self.fetch_func = fetch_func
        self.args = args
        
    def run(self):
        try:
            data = self.fetch_func(*self.args)
            self.data_loaded.emit(data)
        except Exception as e:
            print(f"Lỗi trong luồng tải dữ liệu: {e}")
            self.data_loaded.emit(None)

class EditQuestionDialog(QDialog):
    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.question = question
        self.setWindowTitle(f"Chỉnh sửa câu hỏi ID: {question.id}")
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Danh mục:"))
        self.cat_combo = QComboBox()
        categories = Category.get_all()
        for cat in categories:
            self.cat_combo.addItem(cat.name, cat.id)
            if cat.id == self.question.category_id:
                self.cat_combo.setCurrentIndex(self.cat_combo.count() - 1)
        layout.addWidget(self.cat_combo)

        layout.addWidget(QLabel("Nội dung câu hỏi:"))
        self.text_input = QTextEdit()
        self.text_input.setText(self.question.text)
        layout.addWidget(self.text_input)

        layout.addWidget(QLabel("Độ khó:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem("Dễ", "Easy")
        self.difficulty_combo.addItem("Trung bình", "Medium")
        self.difficulty_combo.addItem("Khó", "Hard")
        # Set current difficulty
        index = self.difficulty_combo.findData(self.question.difficulty)
        if index >= 0:
            self.difficulty_combo.setCurrentIndex(index)
        layout.addWidget(self.difficulty_combo)

        layout.addWidget(QLabel("Các lựa chọn đáp án:"))
        self.choices_layout = QVBoxLayout()
        self.choice_inputs = []
        for i in range(4):
            h_layout = QHBoxLayout()
            c_input = QLineEdit()
            is_correct_btn = QPushButton("Đúng?")
            is_correct_btn.setCheckable(True)
            is_correct_btn.setFixedWidth(60)
            
            if i < len(self.question.answers):
                c_input.setText(self.question.answers[i].text)
                is_correct_btn.setChecked(self.question.answers[i].is_correct)
            
            h_layout.addWidget(c_input)
            h_layout.addWidget(is_correct_btn)
            self.choices_layout.addLayout(h_layout)
            self.choice_inputs.append((c_input, is_correct_btn))
        layout.addLayout(self.choices_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Lưu thay đổi")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        cat_id = self.cat_combo.currentData()
        text = self.text_input.toPlainText()
        diff = self.difficulty_combo.currentData()
        choices = []
        for c_input, is_correct_btn in self.choice_inputs:
            c_text = c_input.text()
            if c_text:
                choices.append((c_text, is_correct_btn.isChecked()))
        return cat_id, text, diff, choices

class AdminDashboard(QWidget):
    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Tiêu đề
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel(f"Quản trị viên: {self.user.username}")
        self.welcome_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #007bff;")
        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.setObjectName("logout_btn") # Áp dụng style màu đỏ
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.on_logout)
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        self.main_layout.addLayout(header_layout)

        # Các tab
        self.tabs = QTabWidget()
        
        # Tab 1: Danh mục & Thêm câu hỏi
        self.tab1 = QWidget()
        self.setup_tab1()
        self.tabs.addTab(self.tab1, "Thêm Câu hỏi")

        # Tab 2: Quản lý câu hỏi hiện có
        self.tab2 = QWidget()
        self.setup_tab2()
        self.tabs.addTab(self.tab2, "Quản lý Đề thi")

        # Tab 3: Kết quả
        self.tab3 = QWidget()
        self.setup_tab3()
        self.tabs.addTab(self.tab3, "Kết quả")

        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)
        
        # Làm mới ban đầu - CHỈ GỌI CÁC HÀM CẦN THIẾT
        self.refresh_categories() # Hàm này đã gọi refresh_manage_questions bên trong
        self.refresh_results()

    def setup_tab1(self):
        layout = QVBoxLayout(self.tab1)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Phần danh mục
        cat_group = QFrame()
        cat_group.setFrameShape(QFrame.StyledPanel)
        cat_group.setObjectName("content_card")
        cat_vbox = QVBoxLayout(cat_group)
        
        title1 = QLabel("QUẢN LÝ DANH MỤC (LỚP HỌC)")
        title1.setStyleSheet("font-weight: bold; color: #007bff;")
        cat_vbox.addWidget(title1)
        
        self.cat_name_input = QLineEdit()
        self.cat_name_input.setPlaceholderText("Tên Danh mục (VD: Toán 12)")
        self.cat_desc_input = QLineEdit()
        self.cat_desc_input.setPlaceholderText("Mô tả")
        self.add_cat_btn = QPushButton("Thêm Danh mục")
        self.add_cat_btn.setCursor(Qt.PointingHandCursor)
        self.add_cat_btn.clicked.connect(self.add_category)
        
        cat_vbox.addWidget(self.cat_name_input)
        cat_vbox.addWidget(self.cat_desc_input)
        cat_vbox.addWidget(self.add_cat_btn)
        layout.addWidget(cat_group)

        # Phần Thêm Câu hỏi
        q_group = QFrame()
        q_group.setFrameShape(QFrame.StyledPanel)
        q_group.setObjectName("content_card")
        q_vbox = QVBoxLayout(q_group)
        
        title2 = QLabel("THÊM CÂU HỎI MỚI")
        title2.setStyleSheet("font-weight: bold; color: #007bff;")
        q_vbox.addWidget(title2)
        
        self.q_cat_combo = QComboBox()
        self.q_text_input = QTextEdit()
        self.q_text_input.setPlaceholderText("Nội dung câu hỏi")
        self.q_text_input.setMaximumHeight(100)
        
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
            is_correct_btn.setFixedWidth(60)
            is_correct_btn.setCursor(Qt.PointingHandCursor)
            h_layout.addWidget(c_input)
            h_layout.addWidget(is_correct_btn)
            self.choices_layout.addLayout(h_layout)
            self.choice_inputs.append((c_input, is_correct_btn))

        h_btn_layout = QHBoxLayout()
        self.add_q_btn = QPushButton("Thêm Câu hỏi")
        self.add_q_btn.setCursor(Qt.PointingHandCursor)
        self.add_q_btn.clicked.connect(self.add_question)
        self.import_pdf_btn = QPushButton("Nhập từ PDF")
        self.import_pdf_btn.setCursor(Qt.PointingHandCursor)
        self.import_pdf_btn.clicked.connect(self.import_from_pdf)
        h_btn_layout.addWidget(self.add_q_btn)
        h_btn_layout.addWidget(self.import_pdf_btn)

        q_vbox.addWidget(QLabel("Chọn Danh mục:"))
        q_vbox.addWidget(self.q_cat_combo)
        q_vbox.addWidget(QLabel("Nội dung câu hỏi:"))
        q_vbox.addWidget(self.q_text_input)
        q_vbox.addWidget(QLabel("Độ khó:"))
        q_vbox.addWidget(self.difficulty_combo)
        q_vbox.addLayout(self.choices_layout)
        q_vbox.addLayout(h_btn_layout)
        layout.addWidget(q_group)

    def setup_tab2(self):
        layout = QVBoxLayout(self.tab2)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("QUẢN LÝ ĐỀ THI")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #007bff;")
        layout.addWidget(title)
        
        filter_layout = QHBoxLayout()
        self.manage_cat_combo = QComboBox()
        self.manage_cat_combo.currentIndexChanged.connect(self.refresh_manage_questions)
        filter_layout.addWidget(QLabel("Lọc theo danh mục:"))
        filter_layout.addWidget(self.manage_cat_combo)
        layout.addLayout(filter_layout)
        
        # Bảng câu hỏi
        self.q_table = QTableWidget()
        self.q_table.setColumnCount(4)
        self.q_table.setHorizontalHeaderLabels(["ID", "Nội dung câu hỏi", "Độ khó", "Thao tác"])
        self.q_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.q_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.q_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.q_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.q_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.q_table)

        self.loading_label = QLabel("Đang tải dữ liệu...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        h_layout = QHBoxLayout()
        self.refresh_q_btn = QPushButton("Làm mới danh sách")
        self.refresh_q_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_q_btn.clicked.connect(self.refresh_manage_questions)
        
        h_layout.addWidget(self.refresh_q_btn)
        layout.addLayout(h_layout)

    def setup_tab3(self):
        layout = QVBoxLayout(self.tab3)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("KẾT QUẢ HỌC SINH")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #007bff;")
        layout.addWidget(title)
        
        # Thống kê nhanh
        self.stats_label = QLabel("Đang tải thống kê...")
        self.stats_label.setObjectName("stats_label")
        self.stats_label.setStyleSheet("padding: 15px; border-radius: 8px; border: 1px solid #007bff; background: rgba(0, 123, 255, 0.1);")
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)

        self.res_list = QListWidget()
        layout.addWidget(self.res_list)

        h_layout = QHBoxLayout()
        self.refresh_results_btn = QPushButton("Làm mới kết quả")
        self.refresh_results_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_results_btn.clicked.connect(self.refresh_results)
        self.export_res_btn = QPushButton("Xuất ra CSV")
        self.export_res_btn.setCursor(Qt.PointingHandCursor)
        self.export_res_btn.clicked.connect(self.export_to_csv)
        
        h_layout.addWidget(self.refresh_results_btn)
        h_layout.addWidget(self.export_res_btn)
        layout.addLayout(h_layout)

    def refresh_categories(self):
        self.manage_cat_combo.blockSignals(True)
        self.q_cat_combo.clear()
        self.manage_cat_combo.clear()
        categories = Category.get_all()
        for cat in categories:
            self.q_cat_combo.addItem(cat.name, cat.id)
            self.manage_cat_combo.addItem(cat.name, cat.id)
        self.manage_cat_combo.blockSignals(False)
        
        # Sau khi nạp xong mới gọi nạp câu hỏi 1 lần duy nhất
        self.refresh_manage_questions()

    def refresh_manage_questions(self):
        cat_id = self.manage_cat_combo.currentData()
        if cat_id is None: return
        
        # Nếu đang có luồng chạy, hãy đợi nó xong hoặc ngắt kết nối
        if hasattr(self, 'loader') and self.loader.isRunning():
            self.loader.data_loaded.disconnect()
            self.loader.wait()

        self.q_table.setRowCount(0)
        self.loading_label.show()
        
        self.loader = DataLoader(Question.get_by_category, cat_id)
        self.loader.data_loaded.connect(self.on_questions_loaded)
        self.loader.start()

    def on_questions_loaded(self, questions):
        self.loading_label.hide()
        for q in questions:
            row = self.q_table.rowCount()
            self.q_table.insertRow(row)
            
            # ID
            self.q_table.setItem(row, 0, QTableWidgetItem(str(q.id)))
            
            # Text
            text_item = QTableWidgetItem(q.text)
            text_item.setToolTip(q.text)
            self.q_table.setItem(row, 1, text_item)
            
            # Difficulty
            diff_text = {"Easy": "Dễ", "Medium": "Trung bình", "Hard": "Khó"}.get(q.difficulty, q.difficulty)
            self.q_table.setItem(row, 2, QTableWidgetItem(diff_text))
            
            # Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(5)
            
            edit_btn = QPushButton("Sửa")
            edit_btn.setFixedWidth(50)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(lambda checked=False, q_obj=q: self.edit_question(q_obj))
            
            delete_btn = QPushButton("Xóa")
            delete_btn.setFixedWidth(50)
            delete_btn.setObjectName("delete_btn")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.clicked.connect(lambda checked=False, q_id=q.id: self.delete_question(q_id))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            self.q_table.setCellWidget(row, 3, action_widget)

    def edit_question(self, question):
        dialog = EditQuestionDialog(question, self)
        if dialog.exec() == QDialog.Accepted:
            cat_id, text, diff, choices = dialog.get_data()
            if Question.update_question(question.id, cat_id, text, diff, choices):
                QMessageBox.information(self, "Thành công", "Đã cập nhật câu hỏi.")
                self.refresh_manage_questions()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể cập nhật câu hỏi.")

    def delete_question(self, q_id=None):
        if q_id is None:
            # Nếu gọi từ nút cũ không truyền tham số (fallback)
            selected_row = self.q_table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn câu hỏi cần xóa.")
                return
            q_id = int(self.q_table.item(selected_row, 0).text())
            
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa câu hỏi ID {q_id}?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            if Question.delete(q_id):
                QMessageBox.information(self, "Thành công", "Đã xóa câu hỏi.")
                self.refresh_manage_questions()

    def refresh_results(self):
        from core.test import ResultHistory, PerformanceAnalyzer
        self.res_list.clear()
        self.stats_label.setText("Đang tải và tính toán kết quả...")
        
        # Hàm gom nhóm logic lấy dữ liệu và tính toán
        def fetch_and_analyze():
            from core.test import ResultHistory, PerformanceAnalyzer
            results = ResultHistory.get_all_results()
            stats = PerformanceAnalyzer.calculate_stats(results)
            return results, stats

        self.results_loader = DataLoader(fetch_and_analyze)
        self.results_loader.data_loaded.connect(self.on_results_loaded)
        self.results_loader.start()

    def on_results_loaded(self, data):
        results, stats = data
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

