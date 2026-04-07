from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ServerOfflineWidget(QWidget):
    def __init__(self, on_retry):
        super().__init__()
        self.on_retry = on_retry
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel("📡")
        icon_label.setStyleSheet("font-size: 72px;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        msg_label = QLabel("Máy chủ chưa trực tuyến")
        msg_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #555;")
        msg_label.setAlignment(Qt.AlignCenter)
        
        detail_label = QLabel("Vui lòng kiểm tra kết nối hoặc liên hệ với quản trị viên.")
        detail_label.setAlignment(Qt.AlignCenter)
        
        self.retry_btn = QPushButton("Thử kết nối lại")
        self.retry_btn.setFixedWidth(200)
        self.retry_btn.clicked.connect(self.on_retry)
        
        layout.addWidget(icon_label)
        layout.addWidget(msg_label)
        layout.addWidget(detail_label)
        layout.addSpacing(20)
        layout.addWidget(self.retry_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
