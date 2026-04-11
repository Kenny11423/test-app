# File: core/network.py - Xử lý kết nối và quản lý đường hầm Ngrok.
import platform
import json
import urllib.request
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
        self.check_connection()
        self.timer.start(self.interval)

    def stop(self):
        self.timer.stop()

    def is_ngrok_running(self):
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output('tasklist /FI "IMAGENAME eq ngrok.exe"', shell=True).decode()
                return "ngrok.exe" in output
            else:
                output = subprocess.check_output(['pgrep', 'ngrok']).decode()
                return len(output.strip()) > 0
        except Exception:
            return False

    def get_ngrok_tunnel_address(self):
        """Fetches the current active TCP tunnel from ngrok's local API."""
        try:
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as response:
                data = json.loads(response.read().decode())
                for tunnel in data.get('tunnels', []):
                    if tunnel.get('proto') == 'tcp':
                        # Example public_url: tcp://0.tcp.ap.ngrok.io:12345
                        addr = tunnel.get('public_url').replace('tcp://', '').split(':')
                        return addr[0], int(addr[1])
        except Exception:
            pass
        return None, None

    def get_db_config(self):
        try:
            with open("db.txt", "r") as f:
                lines = [l.strip() for l in f.readlines()]
                if len(lines) >= 5:
                    return {
                        "host": lines[0],
                        "port": int(lines[1]),
                        "user": lines[2],
                        "password": lines[3],
                        "database": lines[4]
                    }
        except Exception:
            pass
        return None

    def check_connection(self):
        config = self.get_db_config()
        if not config:
            if self.is_online:
                self.is_online = False
                self.status_changed.emit(False)
            return

        ngrok_active = self.is_ngrok_running()
        
        # 1. Nếu ngrok đang chạy cục bộ, tự động cập nhật cấu hình
        if ngrok_active:
            ngrok_host, ngrok_port = self.get_ngrok_tunnel_address()
            if ngrok_host and ngrok_port:
                # Nếu địa chỉ đã thay đổi, cập nhật file db.txt
                if config["host"] != ngrok_host or config["port"] != ngrok_port:
                    config["host"] = ngrok_host
                    config["port"] = ngrok_port
                    try:
                        with open("db.txt", "w") as f:
                            f.write(f"{ngrok_host}\n")
                            f.write(f"{ngrok_port}\n")
                            f.write(f"{config['user']}\n")
                            f.write(f"{config['password']}\n")
                            f.write(f"{config['database']}\n")
                            f.write("ONLINE")
                    except Exception as e:
                        print(f"Error updating db.txt: {e}")
        
        # 2. Try to connect with the current config (manual or auto-updated)
        db_connected = db_manager.connect(**config)
        if db_connected:
            db_manager.run_schema("database/schema.sql")
        
        # The app is "online" if the database is connected.
        # We don't strictly require ngrok to be running locally on the client laptop.
        online = db_connected
        
        if online != self.is_online:
            self.is_online = online
            self.status_changed.emit(online)
