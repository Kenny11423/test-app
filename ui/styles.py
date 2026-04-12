# File: ui/styles.py - Chứa các bộ mã QSS cho chế độ Sáng và Tối.

COMMON_STYLE = """
* {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
}
QMainWindow {
    border-radius: 10px;
}
QPushButton {
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    padding: 6px;
    border-radius: 4px;
    border: 1px solid #ccc;
}
QTabWidget::pane {
    border: 1px solid #ddd;
    border-radius: 4px;
    top: -1px;
}
QTabBar::tab {
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QListWidget {
    border-radius: 4px;
    padding: 5px;
}
QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #eee;
}
QListWidget::item:last {
    border-bottom: none;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    border: 1px solid #ddd;
    border-radius: 12px;
}
"""

LIGHT_STYLE = COMMON_STYLE + """
QWidget {
    background-color: #f8f9fa;
    color: #212529;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    background-color: white;
    border: 1px solid #dee2e6;
}
QLabel#stats_label {
    background-color: #e7f1ff;
    color: #0056b3;
    border: 1px solid #b3d7ff;
}
QLabel {
    color: #212529;
}
QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
}
QPushButton:hover {
    background-color: #0069d9;
}
QPushButton#logout_btn, QPushButton#delete_btn {
    background-color: #dc3545;
}
QPushButton#logout_btn:hover, QPushButton#delete_btn:hover {
    background-color: #c82333;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: white;
    border: 1px solid #ced4da;
    color: #495057;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #80bdff;
}
QTabBar::tab {
    background-color: #e9ecef;
    color: #495057;
}
QTabBar::tab:selected {
    background-color: white;
    border: 1px solid #ddd;
    border-bottom: none;
}
QListWidget {
    background-color: white;
    border: 1px solid #dee2e6;
}
QListWidget::item:selected {
    background-color: #e7f1ff;
    color: #0056b3;
}
"""

DARK_STYLE = COMMON_STYLE + """
QWidget {
    background-color: #212529;
    color: #f8f9fa;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    background-color: #2c3034;
    border: 1px solid #495057;
}
QLabel#stats_label {
    background-color: #343a40;
    color: #0d6efd;
    border: 1px solid #0d6efd;
}
QLabel {
    color: #f8f9fa;
}
QPushButton {
    background-color: #0d6efd;
    color: white;
    border: none;
}
QPushButton:hover {
    background-color: #0b5ed7;
}
QPushButton#logout_btn, QPushButton#delete_btn {
    background-color: #bb2d3b;
}
QPushButton#logout_btn:hover, QPushButton#delete_btn:hover {
    background-color: #a52834;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #343a40;
    border: 1px solid #495057;
    color: #f8f9fa;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #0d6efd;
}
QTabBar::tab {
    background-color: #343a40;
    color: #adb5bd;
}
QTabBar::tab:selected {
    background-color: #495057;
    color: white;
    border: 1px solid #6c757d;
    border-bottom: none;
}
QListWidget {
    background-color: #343a40;
    border: 1px solid #495057;
}
QListWidget::item {
    border-bottom: 1px solid #495057;
}
QListWidget::item:selected {
    background-color: #0d6efd;
    color: white;
}
"""
