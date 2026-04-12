# File: ui/login.py - Giao diện người dùng cho chức năng đăng nhập và đăng ký.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QFrame, QHBoxLayout)
from PySide6.QtCore import Qt
from core.user import UserManager

class LoginWidget(QWidget):
    def __init__(self, on_login_success, on_switch_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_switch_register = on_switch_register
        self.init_ui()

    def init_ui(self):
        # Layout chính chứa card ở giữa
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Container dạng Card
        self.card = QFrame()
        self.card.setFixedWidth(350)
        self.card.setObjectName("login_card")
        self.card.setFrameShape(QFrame.StyledPanel)
        
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 40, 30, 40)
        self.card_layout.setSpacing(20)

        # Tiêu đề
        self.title_label = QLabel("ĐĂNG NHẬP")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.card_layout.addWidget(self.title_label)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFixedHeight(40)
        self.card_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.card_layout.addWidget(self.password_input)

        # Login Button
        self.login_btn = QPushButton("Đăng nhập")
        self.login_btn.setFixedHeight(45)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        self.card_layout.addWidget(self.login_btn)

        # Register Link
        self.register_btn = QPushButton("Chưa có tài khoản? Đăng ký ngay")
        self.register_btn.setFlat(True)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet("color: #007bff; text-decoration: underline; background: transparent;")
        self.register_btn.clicked.connect(self.on_switch_register)
        self.card_layout.addWidget(self.register_btn)

        self.main_layout.addWidget(self.card)

    def handle_login(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            if not username or not password:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
                return
                
            user = UserManager.login_user(username, password)
            if user:
                self.on_login_success(user)
            else:
                QMessageBox.warning(self, "Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Đã xảy ra lỗi nghiêm trọng khi đăng nhập:\n{str(e)}")

class RegisterWidget(QWidget):
    def __init__(self, on_register_success, on_switch_login):
        super().__init__()
        self.on_register_success = on_register_success
        self.on_switch_login = on_switch_login
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Container dạng Card
        self.card = QFrame()
        self.card.setFixedWidth(350)
        self.card.setObjectName("register_card")
        self.card.setFrameShape(QFrame.StyledPanel)
        
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 40, 30, 40)
        self.card_layout.setSpacing(20)

        # Tiêu đề
        self.title_label = QLabel("ĐĂNG KÝ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.card_layout.addWidget(self.title_label)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFixedHeight(40)
        self.card_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.card_layout.addWidget(self.password_input)

        # Role
        self.role_combo = QComboBox()
        self.role_combo.setFixedHeight(40)
        self.role_combo.addItem("Học sinh", "Student")
        self.role_combo.addItem("Quản trị viên", "Admin")
        self.card_layout.addWidget(self.role_combo)

        # Register Button
        self.register_btn = QPushButton("Đăng ký")
        self.register_btn.setFixedHeight(45)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.clicked.connect(self.handle_register)
        self.card_layout.addWidget(self.register_btn)

        # Back to Login
        self.back_btn = QPushButton("Quay lại Đăng nhập")
        self.back_btn.setFlat(True)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("color: #007bff; text-decoration: underline; background: transparent;")
        self.back_btn.clicked.connect(self.on_switch_login)
        self.card_layout.addWidget(self.back_btn)

        self.main_layout.addWidget(self.card)

    def handle_register(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            role = self.role_combo.currentData()
            
            if not username or not password:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return

            if UserManager.register_user(username, password, role):
                QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bây giờ bạn có thể đăng nhập.")
                self.on_switch_login()
            else:
                QMessageBox.warning(self, "Lỗi", "Đăng ký thất bại. Tên đăng nhập có thể đã tồn tại.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Đã xảy ra lỗi nghiêm trọng khi đăng ký:\n{str(e)}")
