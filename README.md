# Test Prep App Online (Python + PySide6 + MySQL)

Ứng dụng ôn thi trắc nghiệm chuyên nghiệp, hoạt động mượt mà như một ứng dụng web. Yêu cầu kết nối với máy chủ MySQL để hoạt động và xử lý linh hoạt trạng thái "Ngoại tuyến" (Offline).

##  Tính Năng Chính
- **Giám Sát Thời Gian Thực**: Tự động phát hiện khi máy chủ trực tuyến/ngoại tuyến và chuyển đổi giao diện tương ứng.
- **Tích Hợp AI (Gemini)**: Tự động tạo câu hỏi trắc nghiệm thông minh theo chủ đề và độ khó yêu cầu bằng công nghệ AI của Google.
- **Nhập Dữ Liệu Từ PDF**: Hỗ trợ trích xuất và nhập câu hỏi tự động từ các tệp đề thi PDF.
- **Đa Nền Tảng**: Thiết kế để kết nối với bất kỳ máy chủ MySQL nào (Localhost, Cloud hoặc Mạng nội bộ).
- **Phân Quyền Người Dùng**:
  - **Admin (Quản trị viên)**: Quản lý danh mục, tạo/sửa câu hỏi, nhập từ PDF, tạo câu hỏi bằng AI và xuất kết quả sinh viên ra CSV.
  - **Student (Sinh viên)**: Làm bài thi tính giờ, xem lịch sử làm bài và nhận kết quả tức thì.
- **Bảo Mật**: Mã hóa mật khẩu bằng thư viện `bcrypt`.

##  Cấu Trúc Dự Án
- `main.py`: **Client Chính.** Giám sát file `db.txt` và máy chủ MySQL. Chỉ cho phép đăng nhập khi Admin đã "Xuất bản" ứng dụng và kết nối được database.
- `server_admin.py`: **Bảng Điều Khiển.** Dùng để cấu hình MySQL, khởi tạo schema database và bật/tắt trạng thái ứng dụng (Online/Offline).
- `core/`:
    - `ai_handler.py`: Xử lý tạo câu hỏi tự động bằng Gemini AI.
    - `pdf_handler.py`: Xử lý đọc và trích xuất nội dung từ tệp PDF.
    - `network.py`: Giám sát trạng thái kết nối máy chủ trong nền.
    - `question.py`, `test.py`, `user.py`: Các logic nghiệp vụ về câu hỏi, bài thi và người dùng.
- `database/manager.py`: Xử lý kết nối và truy vấn MySQL (Singleton).
- `ui/`: Các thành phần giao diện (Login, Admin Dashboard, Student Dashboard, Offline screen).
- `scripts/`: Các công cụ hỗ trợ như nhập liệu PDF (`pdf_importer.py`), thiết lập danh mục (`setup_categories.py`).

##  Cài Đặt & Thiết Lập

### 1. Yêu cầu hệ thống
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

### 4. Chạy ứng dụng
Chạy ứng dụng chính:
   ```bash
   python main.py
   ```

### Tính Năng Của Admin
1. Đăng ký tài khoản với vai trò **Admin**.
2. Quản lý **Danh mục** (VD: Tiếng Anh, Lập trình).
3. Thêm câu hỏi:
   - Nhập thủ công.
   - Sử dụng **AI Generator** để tạo câu hỏi tự động theo chủ đề.
   - Sử dụng **PDF Importer** để nhập từ tệp PDF có sẵn.
4. Xem và xuất kết quả của sinh viên.

### Tính Năng Của Sinh Viên
1. Đăng ký tài khoản với vai trò **Student**.
2. Chọn danh mục và nhấn **Bắt đầu làm bài**.
3. Hoàn thành bài thi trước khi **Đồng hồ đếm ngược** kết thúc.
4. Xem lại lịch sử và tiến độ trong mục **Kết quả cũ**.
