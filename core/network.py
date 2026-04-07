from PySide6.QtCore import QObject, QTimer, Signal
from database.manager import db_manager

class ServerStatusMonitor(QObject):
    status_changed = Signal(bool)

    def __init__(self, interval_ms=5000):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_connection)
        self.interval = interval_ms
        self.is_online = False

    def start(self):
        self.timer.start(self.interval)

    def stop(self):
        self.timer.stop()

    def get_db_config(self):
        try:
            with open("db.txt", "r") as f:
                lines = [l.strip() for l in f.readlines()]
                if len(lines) >= 6:
                    return {
                        "host": lines[0],
                        "port": int(lines[1]),
                        "user": lines[2],
                        "password": lines[3],
                        "database": lines[4]
                    }, lines[5] == "ONLINE"
        except Exception:
            pass
        return None, False

    def check_connection(self):
        config, is_public = self.get_db_config()
        
        if not config or not is_public:
            online = False
        else:
            online = db_manager.connect(**config)
        
        if online != self.is_online:
            self.is_online = online
            self.status_changed.emit(online)
