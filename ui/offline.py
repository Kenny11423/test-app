# File: ui/offline.py - Giao diện hiển thị khi mất kết nối máy chủ.
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt

class ServerOfflineWidget(QWidget):
    def __init__(self, on_retry):
        super().__init__()
        self.on_retry = on_retry
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        
        self.card = QFrame()
        self.card.setFixedWidth(400)
        self.card.setObjectName("offline_card")
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)

        self.icon_label = QLabel("⚠️")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 64px;")
        self.card_layout.addWidget(self.icon_label)

        self.label = QLabel("Mất kết nối với máy chủ!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e74c3c;")
        self.card_layout.addWidget(self.label)

        self.desc = QLabel("Vui lòng kiểm tra lại kết nối mạng hoặc đảm bảo máy chủ đang hoạt động.")
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.desc)

        self.retry_btn = QPushButton("Thử kết nối lại")
        self.retry_btn.setFixedHeight(45)
        self.retry_btn.setCursor(Qt.PointingHandCursor)
        self.retry_btn.clicked.connect(self.on_retry)
        self.card_layout.addWidget(self.retry_btn)

        self.layout.addWidget(self.card)
