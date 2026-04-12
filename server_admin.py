import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QCheckBox, QHBoxLayout)
from PySide6.QtCore import Qt
from database.manager import db_manager

class ServerAdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản trị Máy chủ & Cơ sở dữ liệu")
        self.setFixedSize(400, 550)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Cấu hình kết nối
        self.layout.addWidget(QLabel("### Cấu hình kết nối MySQL"))
        
        self.host = QLineEdit("localhost")
        self.port = QLineEdit("3306")
        self.user = QLineEdit("root")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.database = QLineEdit("test_prep_db")
        
        self.layout.addWidget(QLabel("Máy chủ (Host):"))
        self.layout.addWidget(self.host)
        self.layout.addWidget(QLabel("Cổng (Port):"))
        self.layout.addWidget(self.port)
        self.layout.addWidget(QLabel("Người dùng (User):"))
        self.layout.addWidget(self.user)
        self.layout.addWidget(QLabel("Mật khẩu (Password):"))
        self.layout.addWidget(self.password)
        self.layout.addWidget(QLabel("Cơ sở dữ liệu (Database):"))
        self.layout.addWidget(self.database)
        
        # Các hành động
        h_layout = QHBoxLayout()
        self.test_btn = QPushButton("Kiểm tra kết nối")
        self.test_btn.clicked.connect(self.test_connection)
        self.init_db_btn = QPushButton("Khởi tạo Schema")
        self.init_db_btn.clicked.connect(self.initialize_database)
        h_layout.addWidget(self.test_btn)
        h_layout.addWidget(self.init_db_btn)
        self.layout.addLayout(h_layout)
        
        self.layout.addSpacing(20)
        self.layout.addWidget(QLabel("### Trạng thái công khai của App"))
        self.public_check = QCheckBox("Công khai App (Trực tuyến)")
        self.public_check.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.public_check)
        
        self.save_btn = QPushButton("Lưu & Cập nhật Trạng thái")
        self.save_btn.setFixedHeight(50)
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_btn)
        
        self.load_settings()

    def test_connection(self):
        config = self.get_config()
        if db_manager.connect(**config):
            QMessageBox.information(self, "Thành công", "Kết nối tới MySQL thành công!")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối tới MySQL.")

    def initialize_database(self):
        config = self.get_config()
        if db_manager.connect(**config):
            if db_manager.run_schema("database/schema.sql"):
                QMessageBox.information(self, "Thành công", "Đã khởi tạo cơ sở dữ liệu!")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể chạy file schema.")
        else:
            QMessageBox.critical(self, "Lỗi", "Vui lòng kết nối tới MySQL trước.")

    def get_config(self):
        return {
            "host": self.host.text(),
            "port": int(self.port.text() or 3306),
            "user": self.user.text(),
            "password": self.password.text(),
            "database": self.database.text()
        }

    def save_settings(self):
        config = self.get_config()
        is_public = self.public_check.isChecked()
        
        try:
            with open("db.txt", "w") as f:
                f.write(f"{config['host']}\n")
                f.write(f"{config['port']}\n")
                f.write(f"{config['user']}\n")
                f.write(f"{config['password']}\n")
                f.write(f"{config['database']}\n")
                f.write(f"{'ONLINE' if is_public else 'OFFLINE'}")
            QMessageBox.information(self, "Thành công", "Đã lưu cài đặt và cập nhật trạng thái!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu cài đặt: {e}")

    def load_settings(self):
        try:
            with open("db.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 5:
                    self.host.setText(lines[0].strip())
                    self.port.setText(lines[1].strip())
                    self.user.setText(lines[2].strip())
                    self.password.setText(lines[3].strip())
                    self.database.setText(lines[4].strip())
                if len(lines) >= 6:
                    self.public_check.setChecked(lines[5].strip() == "ONLINE")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerAdminApp()
    window.show()
    sys.exit(app.exec())
