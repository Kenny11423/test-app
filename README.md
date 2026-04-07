# Test Prep App Online (Python + PySide6 + MySQL)

A professional multiple-choice test preparation application that functions like a web app. It requires a connection to a MySQL server host to operate and handles "Offline" states gracefully.

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
- Access to a MySQL Server (Local or Remote)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database & Server Setup
1. Run the **Server Admin** app:
   ```bash
   python server_admin.py
   ```
2. Enter your MySQL credentials.
3. Click **"Test Connection"** to verify.
4. Click **"Run Schema"** to initialize the database tables.
5. Check **"Publish App (Online)"** and click **"Save & Update Status"**.

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
