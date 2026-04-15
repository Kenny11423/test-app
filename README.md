# Test Prep App Online (Python + PySide6 + MySQL)

Ứng dụng ôn thi trắc nghiệm chuyên nghiệp, hoạt động mượt mà như một ứng dụng web. Yêu cầu kết nối với máy chủ MySQL để hoạt động và xử lý linh hoạt trạng thái "Ngoại tuyến" (Offline).

## 🌟 Key Features
- **Web-Like Connectivity**: The app remains on a "Server Offline" page until it can successfully reach the database host.
- **Real-Time Monitoring**: Automatically detects when the server goes online/offline and transitions the UI accordingly.
- **Multi-Platform Ready**: Designed to connect to any MySQL host (Localhost, Cloud, or Local Network).
- **Role-Based Access**:
  - **Admin**: Manage categories, create questions, and export student results to CSV.
  - **Student**: Take timed tests, view performance history, and get instant scoring.
- **Secure Auth**: Password hashing using `bcrypt`.

## 🏗️ Project Architecture
- `server_admin.py`: **The Control Panel.** Use this to configure MySQL settings, initialize the database schema, and "Publish" the app (toggle Online/Offline).
- `main.py`: **The Main Client.** This app monitors `db.txt` and the MySQL server. it only allows login when the Server Admin has published the app and the database is reachable.
- `database/manager.py`: Singleton MySQL connection and query handler.
- `core/network.py`: Background monitor for server and status availability.
- `ui/offline.py`: Dedicated "Server is not online" interface.
- `ui/`: Modular UI components for Login, Admin, and Student dashboards.

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.8+
- Máy chủ MySQL (Local hoặc Remote)
- API Key của Google Gemini (nếu muốn dùng tính năng AI)

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```
Các thư viện chính bao gồm: `mysql-connector-python`, `PySide6`, `bcrypt`, `pymupdf`, `numpy`, `PyQtWebEngine`, `matplotlib`.

### 3. Cấu hình AI (Tùy chọn)
Tạo tệp `ai_key.txt` ở thư mục gốc và dán API Key của Google Gemini vào đó.

### 4. Running the Main App
1. Once the server is published, run the main app:
   ```bash
   python main.py
   ```
2. The app will automatically detect the settings from `db.txt` and transition from the "Offline" screen to the Login screen.

## 📖 How to Use

### Handling "Server Offline"
- If `main.py` shows **"Server is not online"**, it means either the MySQL server is down OR the app has been set to **OFFLINE** in the `server_admin.py` dashboard.
- Use `server_admin.py` to toggle the visibility.

### Admin Tasks
1. Register an account with the **Admin** role.
2. Create **Categories** (e.g., Python, Mathematics).
3. Add **Questions** to categories with 4 choices and 1 correct answer.
4. View/Export results from the **Student Results** section.

### Student Tasks
1. Register an account with the **Student** role.
2. Select a category and click **Start Test**.
3. Complete the test before the **Timer** expires.
4. View your progress in the **Past Results** list.
