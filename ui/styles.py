# File: ui/styles.py - Chứa các bộ mã QSS cho chế độ Sáng và Tối (Phiên bản Nâng cấp).

COMMON_STYLE = """
* {
    font-family: 'Segoe UI', 'SF Pro Display', Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
}
QMainWindow {
    background-color: #f5f7fa;
}
QPushButton {
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
    border: none;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #d1d9e6;
    background-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #4a90e2;
}
QTabWidget::pane {
    border: 1px solid #e0e6ed;
    border-radius: 8px;
    background-color: white;
    top: -1px;
}
QTabBar::tab {
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    background-color: #e0e6ed;
    color: #64748b;
    font-weight: bold;
}
QTabBar::tab:selected {
    background-color: white;
    color: #4a90e2;
    border: 1px solid #e0e6ed;
    border-bottom: none;
}
QListWidget {
    border-radius: 8px;
    padding: 5px;
    border: 1px solid #e0e6ed;
}
QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid #f1f5f9;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #e0f2fe;
    color: #0369a1;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    background-color: white;
    border: 1px solid #e0e6ed;
    border-radius: 16px;
}
QLabel#title_label {
    font-size: 28px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 10px;
}
QLabel#section_title {
    font-size: 18px;
    font-weight: 700;
    color: #4a90e2;
    margin-bottom: 5px;
    padding-bottom: 5px;
}
QHeaderView::section {
    background-color: #f8fafc;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-weight: bold;
    color: #475569;
}
QTableWidget {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    background-color: white;
    alternate-background-color: #f8fafc;
}
QTableWidget QPushButton {
    padding: 4px 12px;
    font-size: 12px;
    min-width: 60px;
    border-radius: 4px;
}
"""

LIGHT_STYLE = COMMON_STYLE + """
QWidget {
    background-color: #f8fafc;
    color: #334155;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    background-color: white;
}
QLabel#stats_label {
    background-color: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}
QPushButton {
    background-color: #4a90e2;
    color: white;
}
QPushButton:hover {
    background-color: #357abd;
}
QPushButton:pressed {
    background-color: #2d669f;
}
QPushButton#logout_btn, QPushButton#delete_btn {
    background-color: #ef4444;
}
QPushButton#logout_btn:hover, QPushButton#delete_btn:hover {
    background-color: #dc2626;
}
QPushButton#ai_btn {
    background-color: #8b5cf6;
}
QPushButton#ai_btn:hover {
    background-color: #7c3aed;
}
"""

DARK_STYLE = COMMON_STYLE + """
QWidget {
    background-color: #0f172a;
    color: #e2e8f0;
}
QMainWindow {
    background-color: #0f172a;
}
QFrame#login_card, QFrame#register_card, QFrame#offline_card, QFrame#content_card, QFrame#header_card, QFrame#question_card {
    background-color: #1e293b;
    border: 1px solid #334155;
}
QLabel#title_label {
    color: #f8fafc;
}
QLabel#stats_label {
    background-color: #1e3a8a;
    color: #60a5fa;
    border: 1px solid #2563eb;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}
QPushButton {
    background-color: #3b82f6;
    color: white;
}
QPushButton:hover {
    background-color: #2563eb;
}
QPushButton#logout_btn, QPushButton#delete_btn {
    background-color: #ef4444;
}
QPushButton#logout_btn:hover, QPushButton#delete_btn:hover {
    background-color: #dc2626;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    color: #f8fafc;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #3b82f6;
}
QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
}
QTabBar::tab:selected {
    background-color: #334155;
    color: #60a5fa;
    border: 1px solid #475569;
}
QTabWidget::pane {
    background-color: #1e293b;
    border: 1px solid #334155;
}
QListWidget {
    background-color: #1e293b;
    border: 1px solid #334155;
}
QListWidget::item {
    border-bottom: 1px solid #334155;
}
QListWidget::item:selected {
    background-color: #1e3a8a;
    color: #60a5fa;
}
QHeaderView::section {
    background-color: #1e293b;
    border-bottom: 2px solid #334155;
    color: #94a3b8;
}
QTableWidget {
    border: 1px solid #334155;
    gridline-color: #334155;
    background-color: #1e293b;
    alternate-background-color: #0f172a;
    color: #f8fafc;
}
QTableWidget::item:selected {
    background-color: #1e3a8a;
    color: #60a5fa;
}
QTableWidget QPushButton {
    color: white;
}
"""

