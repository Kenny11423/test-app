# File: ui/login.py - Giao diện người dùng cho chức năng đăng nhập và đăng ký.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox)
from core.user import UserManager

class LoginWidget(QWidget):
    def __init__(self, on_login_success, on_switch_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_switch_register = on_switch_register
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Đăng nhập vào Ứng dụng Ôn thi")
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Đăng nhập")
        self.login_btn.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Chưa có tài khoản? Đăng ký")
        self.register_btn.clicked.connect(self.on_switch_register)
        self.layout.addWidget(self.register_btn)

        self.setLayout(self.layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = UserManager.login_user(username, password)
        if user:
            self.on_login_success(user)
        else:
            QMessageBox.warning(self, "Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")

class RegisterWidget(QWidget):
    def __init__(self, on_register_success, on_switch_login):
        super().__init__()
        self.on_register_success = on_register_success
        self.on_switch_login = on_switch_login
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Tạo tài khoản mới")
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Admin"]) # Keep internal values or translate display? 
        # Using a mapping for display if needed, but for now I'll just change the items to Vietnamese labels if the logic allows.
        # User.role is compared against 'Admin' in main.py. I should keep internal values but maybe use display text.
        self.role_combo.clear()
        self.role_combo.addItem("Học sinh", "Student")
        self.role_combo.addItem("Quản trị viên", "Admin")
        self.layout.addWidget(self.role_combo)

        self.register_btn = QPushButton("Đăng ký")
        self.register_btn.clicked.connect(self.handle_register)
        self.layout.addWidget(self.register_btn)

        self.back_btn = QPushButton("Quay lại Đăng nhập")
        self.back_btn.clicked.connect(self.on_switch_login)
        self.layout.addWidget(self.back_btn)

        self.setLayout(self.layout)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentData() # Sử dụng dữ liệu thay vì văn bản
        
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        if UserManager.register_user(username, password, role):
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bây giờ bạn có thể đăng nhập.")
            self.on_switch_login()
        else:
            QMessageBox.warning(self, "Lỗi", "Đăng ký thất bại. Tên đăng nhập có thể đã tồn tại.")
