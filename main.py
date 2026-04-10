import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget)
from database.manager import db_manager
from ui.login import LoginWidget, RegisterWidget
from ui.admin_dashboard import AdminDashboard
from ui.student_dashboard import StudentDashboard
from ui.test_session import TestSessionWidget
from ui.offline import ServerOfflineWidget
from core.network import ServerStatusMonitor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Ôn thi Trực tuyến")
        self.resize(800, 600)
        
        # Ensure db.txt exists with some defaults if it doesn't
        self.ensure_db_config()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.user = None
        self.offline_widget = ServerOfflineWidget(self.check_server_connection)
        self.central_widget.addWidget(self.offline_widget)
        
        # Setup Server Monitor
        self.monitor = ServerStatusMonitor()
        self.monitor.status_changed.connect(self.handle_server_status)
        
        # Pre-check before showing UI
        self.monitor.check_connection()
        if self.monitor.is_online:
            self.show_login()
        else:
            self.central_widget.setCurrentWidget(self.offline_widget)
            
        self.monitor.start()

    def ensure_db_config(self):
        if not os.path.exists("db.txt"):
            with open("db.txt", "w") as f:
                # Default local settings: host, port, user, pass, db
                f.write("localhost\n3306\nroot\n\ntest_prep_db\nONLINE")

    def handle_server_status(self, is_online):
        if is_online:
            if not self.user and self.central_widget.currentWidget() == self.offline_widget:
                self.show_login()
        else:
            # If we lose connection, go back to offline screen
            self.user = None
            self.central_widget.setCurrentWidget(self.offline_widget)

    def check_server_connection(self):
        self.monitor.check_connection()

    def show_login(self):
        self.login_widget = LoginWidget(self.on_login_success, self.switch_to_register)
        self.register_widget = RegisterWidget(self.on_register_success, self.switch_to_login)
        
        self.central_widget.addWidget(self.login_widget)
        self.central_widget.addWidget(self.register_widget)
        self.central_widget.setCurrentWidget(self.login_widget)

    def switch_to_register(self):
        self.central_widget.setCurrentWidget(self.register_widget)

    def switch_to_login(self):
        self.central_widget.setCurrentWidget(self.login_widget)

    def on_login_success(self, user):
        self.user = user
        if user.role == 'Admin':
            self.show_admin_dashboard()
        else:
            self.show_student_dashboard()

    def on_register_success(self):
        self.central_widget.setCurrentWidget(self.login_widget)

    def show_admin_dashboard(self):
        self.admin_dash = AdminDashboard(self.user, self.handle_logout)
        self.central_widget.addWidget(self.admin_dash)
        self.central_widget.setCurrentWidget(self.admin_dash)

    def show_student_dashboard(self):
        self.student_dash = StudentDashboard(self.user, self.start_test, self.handle_logout)
        self.central_widget.addWidget(self.student_dash)
        self.central_widget.setCurrentWidget(self.student_dash)

    def start_test(self, category_id):
        self.test_widget = TestSessionWidget(self.user.id, category_id, self.show_student_dashboard)
        self.central_widget.addWidget(self.test_widget)
        self.central_widget.setCurrentWidget(self.test_widget)

    def handle_logout(self):
        self.user = None
        self.show_login()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
