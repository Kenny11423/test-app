from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QTextEdit, 
                             QFormLayout, QHBoxLayout, QListWidget, QSpinBox,
                             QFileDialog, QTabWidget, QListWidgetItem, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView, QDialog)
from core.question import Category, Question
from PySide6.QtCore import Qt, QThread, Signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

class AIDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo câu hỏi bằng AI (Gemini)")
        self.setFixedWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Chủ đề câu hỏi (VD: Lịch sử Việt Nam):"))
        self.topic_input = QLineEdit()
        layout.addWidget(self.topic_input)
        layout.addWidget(QLabel("Số lượng câu hỏi (1-20):"))
        self.num_spin = QSpinBox()
        self.num_spin.setRange(1, 20)
        self.num_spin.setValue(5)
        layout.addWidget(self.num_spin)
        layout.addWidget(QLabel("Độ khó:"))
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["Easy", "Medium", "Hard"])
        layout.addWidget(self.diff_combo)
        layout.addWidget(QLabel("Gemini API Key:"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        if os.path.exists("ai_key.txt"):
            with open("ai_key.txt", "r") as f:
                self.key_input.setText(f.read().strip())
        layout.addWidget(self.key_input)
        self.generate_btn = QPushButton("Bắt đầu tạo")
        self.generate_btn.clicked.connect(self.accept)
        layout.addWidget(self.generate_btn)

    def get_data(self):
        key = self.key_input.text()
        if key:
            with open("ai_key.txt", "w") as f:
                f.write(key)
        return self.topic_input.text(), self.num_spin.value(), self.diff_combo.currentText(), key

class DataLoader(QThread):
    data_loaded = Signal(object)
    def __init__(self, fetch_func, *args):
        super().__init__()
        self.fetch_func = fetch_func
        self.args = args
    def run(self):
        try:
            data = self.fetch_func(*self.args)
            self.data_loaded.emit(data)
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")
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
        layout.addWidget(QLabel("Môn học:"))
        self.cat_combo = QComboBox()
        for cat in Category.get_all():
            self.cat_combo.addItem(cat.name, cat.id)
            if cat.id == self.question.category_id:
                self.cat_combo.setCurrentIndex(self.cat_combo.count() - 1)
        layout.addWidget(self.cat_combo)
        layout.addWidget(QLabel("Lớp:"))
        self.grade_combo = QComboBox()
        for i in range(1, 13):
            self.grade_combo.addItem(f"Lớp {i}", i)
        self.grade_combo.setCurrentIndex(self.question.grade - 1)
        layout.addWidget(self.grade_combo)
        layout.addWidget(QLabel("Nội dung câu hỏi:"))
        self.text_input = QTextEdit()
        self.text_input.setText(self.question.text)
        layout.addWidget(self.text_input)
        layout.addWidget(QLabel("Độ khó:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem("Dễ", "Easy")
        self.difficulty_combo.addItem("Trung bình", "Medium")
        self.difficulty_combo.addItem("Khó", "Hard")
        index = self.difficulty_combo.findData(self.question.difficulty)
        if index >= 0: self.difficulty_combo.setCurrentIndex(index)
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
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Lưu thay đổi")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        choices = []
        for c_input, is_correct_btn in self.choice_inputs:
            if c_input.text(): choices.append((c_input.text(), is_correct_btn.isChecked()))
        return self.cat_combo.currentData(), self.grade_combo.currentData(), self.text_input.toPlainText(), self.difficulty_combo.currentData(), choices

class AdminDashboard(QWidget):
    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.current_theme_mode = 'light'
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel(f"Quản trị viên: {self.user.username}")
        self.welcome_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #007bff;")
        self.logout_btn = QPushButton("Đăng xuất")
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.clicked.connect(self.on_logout)
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        self.main_layout.addLayout(header_layout)
        self.tabs = QTabWidget()
        self.tab1 = QWidget(); self.setup_tab1(); self.tabs.addTab(self.tab1, "Thêm Câu hỏi")
        self.tab2 = QWidget(); self.setup_tab2(); self.tabs.addTab(self.tab2, "Quản lý Đề thi")
        self.tab3 = QWidget(); self.setup_tab3(); self.tabs.addTab(self.tab3, "Kết quả")
        self.main_layout.addWidget(self.tabs)
        self.refresh_categories(); self.refresh_results()

    def toggle_chart_theme(self, theme_mode):
        self.current_theme_mode = theme_mode
        self.refresh_results()

    def setup_tab1(self):
        layout = QVBoxLayout(self.tab1)
        layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(15)
        cat_group = QFrame(); cat_group.setObjectName("content_card"); cat_vbox = QVBoxLayout(cat_group)
        title1 = QLabel("QUẢN LÝ MÔN HỌC"); title1.setStyleSheet("font-weight: bold; color: #007bff;"); cat_vbox.addWidget(title1)
        self.cat_name_input = QLineEdit(); self.cat_name_input.setPlaceholderText("Tên Môn học (VD: Toán)")
        self.cat_desc_input = QLineEdit(); self.cat_desc_input.setPlaceholderText("Mô tả")
        self.add_cat_btn = QPushButton("Thêm Môn học"); self.add_cat_btn.clicked.connect(self.add_category)
        cat_vbox.addWidget(self.cat_name_input); cat_vbox.addWidget(self.cat_desc_input); cat_vbox.addWidget(self.add_cat_btn)
        layout.addWidget(cat_group)
        q_group = QFrame(); q_group.setObjectName("content_card"); q_vbox = QVBoxLayout(q_group)
        title2 = QLabel("THÊM CÂU HỎI MỚI"); title2.setStyleSheet("font-weight: bold; color: #007bff;"); q_vbox.addWidget(title2)
        h_sel = QHBoxLayout()
        self.q_cat_combo = QComboBox(); self.q_grade_combo = QComboBox()
        for i in range(1, 13): self.q_grade_combo.addItem(f"Lớp {i}", i)
        h_sel.addWidget(QLabel("Môn:")); h_sel.addWidget(self.q_cat_combo, 2)
        h_sel.addWidget(QLabel("Lớp:")); h_sel.addWidget(self.q_grade_combo, 1)
        q_vbox.addLayout(h_sel)
        self.q_text_input = QTextEdit(); self.q_text_input.setPlaceholderText("Nội dung câu hỏi"); self.q_text_input.setMaximumHeight(80); q_vbox.addWidget(self.q_text_input)
        self.difficulty_combo = QComboBox(); self.difficulty_combo.addItems(["Easy", "Medium", "Hard"]); q_vbox.addWidget(self.difficulty_combo)
        self.choices_layout = QVBoxLayout(); self.choice_inputs = []
        for i in range(4):
            h_layout = QHBoxLayout(); c_input = QLineEdit(); c_input.setPlaceholderText(f"Lựa chọn {i+1}")
            is_correct_btn = QPushButton("Đúng?"); is_correct_btn.setCheckable(True); is_correct_btn.setFixedWidth(60)
            h_layout.addWidget(c_input); h_layout.addWidget(is_correct_btn); self.choices_layout.addLayout(h_layout); self.choice_inputs.append((c_input, is_correct_btn))
        q_vbox.addLayout(self.choices_layout)
        h_btn_layout = QHBoxLayout()
        self.add_q_btn = QPushButton("Thêm thủ công"); self.add_q_btn.clicked.connect(self.add_question)
        self.import_pdf_btn = QPushButton("Nhập từ PDF"); self.import_pdf_btn.clicked.connect(self.import_from_pdf)
        self.ai_btn = QPushButton("✨ Tạo bằng AI"); self.ai_btn.setStyleSheet("background-color: #6f42c1; color: white;"); self.ai_btn.clicked.connect(self.generate_with_ai)
        h_btn_layout.addWidget(self.add_q_btn); h_btn_layout.addWidget(self.import_pdf_btn); h_btn_layout.addWidget(self.ai_btn)
        q_vbox.addLayout(h_btn_layout); layout.addWidget(q_group)

    def setup_tab2(self):
        layout = QVBoxLayout(self.tab2); layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(15)
        title = QLabel("QUẢN LÝ ĐỀ THI"); title.setStyleSheet("font-weight: bold; font-size: 16px; color: #007bff;"); layout.addWidget(title)
        filter_layout = QHBoxLayout()
        self.manage_cat_combo = QComboBox(); self.manage_grade_combo = QComboBox()
        for i in range(1, 13): self.manage_grade_combo.addItem(f"Lớp {i}", i)
        self.manage_cat_combo.currentIndexChanged.connect(self.refresh_manage_questions)
        self.manage_grade_combo.currentIndexChanged.connect(self.refresh_manage_questions)
        filter_layout.addWidget(QLabel("Môn:")); filter_layout.addWidget(self.manage_cat_combo)
        filter_layout.addWidget(QLabel("Lớp:")); filter_layout.addWidget(self.manage_grade_combo)
        layout.addLayout(filter_layout)
        self.q_table = QTableWidget(); self.q_table.setColumnCount(4); self.q_table.setHorizontalHeaderLabels(["ID", "Nội dung", "Độ khó", "Thao tác"])
        self.q_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.q_table)
        self.loading_label = QLabel("Đang tải..."); self.loading_label.hide(); layout.addWidget(self.loading_label)
        self.refresh_q_btn = QPushButton("Làm mới"); self.refresh_q_btn.clicked.connect(self.refresh_manage_questions); layout.addWidget(self.refresh_q_btn)

    def setup_tab3(self):
        layout = QVBoxLayout(self.tab3); layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(15)
        self.figure = Figure(figsize=(5, 4), dpi=100); self.canvas = FigureCanvas(self.figure); layout.addWidget(self.canvas, 1)
        self.stats_label = QLabel("Đang tải..."); self.stats_label.setObjectName("stats_label"); layout.addWidget(self.stats_label)
        self.res_list = QListWidget(); self.res_list.setMaximumHeight(150); layout.addWidget(self.res_list)
        h_layout = QHBoxLayout(); self.refresh_results_btn = QPushButton("Làm mới"); self.refresh_results_btn.clicked.connect(self.refresh_results)
        self.export_res_btn = QPushButton("Xuất CSV"); self.export_res_btn.clicked.connect(self.export_to_csv)
        h_layout.addWidget(self.refresh_results_btn); h_layout.addWidget(self.export_res_btn); layout.addLayout(h_layout)

    def refresh_categories(self):
        self.manage_cat_combo.blockSignals(True)
        self.q_cat_combo.clear(); self.manage_cat_combo.clear()
        for cat in Category.get_all(force_refresh=True):
            self.q_cat_combo.addItem(cat.name, cat.id); self.manage_cat_combo.addItem(cat.name, cat.id)
        self.manage_cat_combo.blockSignals(False); self.refresh_manage_questions()

    def refresh_manage_questions(self):
        cat_id = self.manage_cat_combo.currentData(); grade = self.manage_grade_combo.currentData()
        if cat_id is None: return
        if hasattr(self, 'loader') and self.loader.isRunning(): self.loader.data_loaded.disconnect(); self.loader.wait()
        self.q_table.setRowCount(0); self.loading_label.show()
        self.loader = DataLoader(Question.get_by_category, cat_id, grade)
        self.loader.data_loaded.connect(self.on_questions_loaded); self.loader.start()

    def on_questions_loaded(self, questions):
        self.loading_label.hide()
        if not questions: return
        for q in questions:
            row = self.q_table.rowCount(); self.q_table.insertRow(row)
            self.q_table.setItem(row, 0, QTableWidgetItem(str(q.id)))
            self.q_table.setItem(row, 1, QTableWidgetItem(q.text))
            diff_map = {"Easy": "Dễ", "Medium": "TB", "Hard": "Khó"}
            self.q_table.setItem(row, 2, QTableWidgetItem(diff_map.get(q.difficulty, q.difficulty)))
            act_w = QWidget(); act_l = QHBoxLayout(act_w); act_l.setContentsMargins(2,2,2,2)
            ed_b = QPushButton("Sửa"); ed_b.setFixedWidth(40); ed_b.clicked.connect(lambda chk=False, qo=q: self.edit_question(qo))
            de_b = QPushButton("Xóa"); de_b.setFixedWidth(40); de_b.setObjectName("delete_btn"); de_b.clicked.connect(lambda chk=False, qi=q.id: self.delete_question(qi))
            act_l.addWidget(ed_b); act_l.addWidget(de_b); self.q_table.setCellWidget(row, 3, act_w)

    def edit_question(self, question):
        dialog = EditQuestionDialog(question, self)
        if dialog.exec() == QDialog.Accepted:
            cat_id, grade, text, diff, choices = dialog.get_data()
            if Question.update_question(question.id, cat_id, grade, text, diff, choices):
                QMessageBox.information(self, "Xong", "Đã cập nhật!"); self.refresh_manage_questions()

    def delete_question(self, q_id=None):
        if q_id is None:
            row = self.q_table.currentRow(); q_id = int(self.q_table.item(row, 0).text()) if row >= 0 else None
        if q_id and QMessageBox.question(self, "Xóa", f"Xóa ID {q_id}?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            if Question.delete(q_id): self.refresh_manage_questions()

    def generate_with_ai(self):
        cat_id = self.q_cat_combo.currentData(); grade = self.q_grade_combo.currentData()
        if not cat_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hoặc thêm Môn học trước khi tạo bằng AI!")
            return
        dialog = AIDialog(self)
        if dialog.exec() == QDialog.Accepted:
            topic, num, diff, key = dialog.get_data()
            if not key:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Gemini API Key!")
                return
            self.ai_btn.setEnabled(False); self.ai_btn.setText("⏳...");
            def run():
                from core.ai_handler import AIGenerator
                return AIGenerator(key).generate_questions(f"{topic} lớp {grade}", num, diff)
            self.ai_loader = DataLoader(run); self.ai_loader.data_loaded.connect(lambda d: self.on_ai_gen(d, cat_id, grade, diff)); self.ai_loader.start()

    def on_ai_gen(self, data, cat_id, grade, diff):
        self.ai_btn.setEnabled(True); self.ai_btn.setText("✨ Tạo bằng AI")
        if not data:
            QMessageBox.warning(self, "Lỗi", "Không thể tạo câu hỏi. Vui lòng kiểm tra API Key hoặc nội dung yêu cầu.")
            return
        for item in data:
            choices = [(c['text'], c.get('is_correct', False)) for c in item['choices']]
            Question.add_question(cat_id, grade, item['text'], diff, choices)
        QMessageBox.information(self, "Xong", "Đã thêm câu hỏi AI!"); self.refresh_manage_questions()

    def import_from_pdf(self):
        cat_id = self.q_cat_combo.currentData(); grade = self.q_grade_combo.currentData()
        if not cat_id: return
        path, _ = QFileDialog.getOpenFileName(self, "Chọn PDF", "", "PDF (*.pdf)")
        if path:
            from core.pdf_handler import update_db_with_pdf
            count = update_db_with_pdf(path, cat_id, grade)
            QMessageBox.information(self, "Xong", f"Đã thêm {count} câu!"); self.refresh_manage_questions()

    def add_category(self):
        name = self.cat_name_input.text()
        if name: Category.add(name, ""); self.cat_name_input.clear(); self.refresh_categories()

    def add_question(self):
        cat_id = self.q_cat_combo.currentData()
        grade = self.q_grade_combo.currentData()
        text = self.q_text_input.toPlainText()
        diff = self.difficulty_combo.currentText()
        
        choices = []
        for c_input, is_correct_btn in self.choice_inputs:
            if c_input.text():
                choices.append((c_input.text(), is_correct_btn.isChecked()))
        
        if not text or not choices:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung câu hỏi và các lựa chọn.")
            return

        if Question.add_question(cat_id, grade, text, diff, choices):
            QMessageBox.information(self, "Thành công", "Đã thêm câu hỏi mới!")
            self.q_text_input.clear()
            for c_input, is_correct_btn in self.choice_inputs:
                c_input.clear()
                is_correct_btn.setChecked(False)
            self.refresh_manage_questions()

    def refresh_results(self):
        self.res_list.clear()
        def fetch():
            from core.test import ResultHistory, PerformanceAnalyzer
            results = ResultHistory.get_all_results(); stats = PerformanceAnalyzer.calculate_stats(results)
            return results, stats
        self.results_loader = DataLoader(fetch); self.results_loader.data_loaded.connect(self.on_results_loaded); self.results_loader.start()

    def on_results_loaded(self, data):
        if not data: return
        results, stats = data; self.figure.clear(); ax = self.figure.add_subplot(111)
        recent = results[:10][::-1]; users = [r['username'][:8] for r in recent]; scores = [(r['score']/r['total_questions'])*100 for r in recent]
        is_dark = self.current_theme_mode == 'dark'
        bg = '#212529' if is_dark else '#f8f9fa'; fg = '#f8f9fa' if is_dark else '#212529'; bc = '#0d6efd' if is_dark else '#007bff'
        self.figure.patch.set_facecolor(bg); ax.set_facecolor(bg); ax.bar(users, scores, color=bc, alpha=0.7); ax.tick_params(colors=fg); ax.set_ylim(0, 105); self.canvas.draw()
        if stats: self.stats_label.setText(f"📊 Tổng: {stats['count']} | TB: {stats['mean']:.1f}%")
        for res in results: self.res_list.addItem(f"{res['username']} | Lớp {res.get('grade','?')} | {res['score']}/{res['total_questions']}")

    def export_to_csv(self):
        import csv; from core.test import ResultHistory; res = ResultHistory.get_all_results()
        if res:
            with open('all_results.csv','w') as f:
                w = csv.DictWriter(f, fieldnames=res[0].keys()); w.writeheader(); w.writerows(res)
            QMessageBox.information(self, "Xong", "Đã xuất CSV!")
