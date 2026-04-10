 📑 Đặc Tả Thiết Kế Chi Tiết: Test Prep App Online

  1. Tổng quan hệ thống (System Overview)
  Hệ thống là một ứng dụng Desktop được thiết kế để quản lý và thực hiện các bài thi trắc nghiệm. Ứng dụng hỗ trợ kết nối từ xa qua tunnel (Ngrok), tự động cấu hình và quản lý
  trạng thái máy chủ theo thời gian thực.

   * Ngôn ngữ: Python 3.8+
   * Giao diện: PySide6 (Qt for Python)
   * Cơ sở dữ liệu: MySQL
   * Kết nối: Tự động dò tìm Ngrok Tunnel API.

  ---

  2. Kiến trúc phần mềm (Software Architecture)

  Hệ thống tuân thủ kiến trúc lớp (Layered Architecture):

   1. Presentation Layer (ui/): Quản lý giao diện người dùng và sự kiện.
   2. Logic Layer (core/): Xử lý nghiệp vụ, kiểm tra kết nối và điều phối dữ liệu.
   3. Data Access Layer (database/): Thực thi các truy vấn SQL và quản lý kết nối Singleton.
   4. External Integration: Kết nối với Ngrok API để lấy thông tin tunnel tự động.

  ---

  3. Thiết kế Cơ sở dữ liệu (Database Design)

  Dựa trên tệp schema.sql, cơ sở dữ liệu bao gồm các thực thể chính sau:

  3.1 Bảng users (Người dùng)

  ┌───────────────┬──────────────┬─────────────────────────────┐
  │ Trường        │ Kiểu dữ liệu │ Đặc tả                      │
  ├───────────────┼──────────────┼─────────────────────────────┤
  │ id            │ INT (PK)     │ Tự động tăng                │
  │ username      │ VARCHAR(255) │ Tên đăng nhập (Unique)      │
  │ password_hash │ VARCHAR(255) │ Mật khẩu đã mã hóa (Bcrypt) │
  │ role          │ ENUM         │ 'Admin' hoặc 'Student'      │
  └───────────────┴──────────────┴─────────────────────────────┘


  3.2 Bảng categories (Danh mục môn học)

  ┌────────┬──────────────┬──────────────────────────────────────┐
  │ Trường │ Kiểu dữ liệu │ Đặc tả                               │
  ├────────┼──────────────┼──────────────────────────────────────┤
  │ id     │ INT (PK)     │ Tự động tăng                         │
  │ name   │ VARCHAR(255) │ Tên môn học (Ví dụ: Python, English) │
  └────────┴──────────────┴──────────────────────────────────────┘


  3.3 Bảng questions & answers
   * Questions: Lưu nội dung câu hỏi, độ khó và liên kết với category_id.
   * Answers: Lưu các lựa chọn và đánh dấu is_correct để xác định đáp án đúng.

  3.4 Bảng test_results (Kết quả thi)
  Lưu lịch sử thi gồm: user_id, category_id, điểm số (score), tổng số câu hỏi và ngày thực hiện.

  ---

  4. Thiết kế các Module chi tiết

  4.1 Module Giám sát Mạng (core/network.py)
  Đây là trái tim của hệ thống tự động hóa:
   * Hàm is_ngrok_running(): Sử dụng subprocess để kiểm tra tiến trình ngrok trong hệ thống.
   * Hàm get_ngrok_tunnel_address(): Truy vấn tới http://127.0.0.1:4040/api/tunnels để lấy thông tin Host và Port công khai mới nhất.
   * Tín hiệu status_changed: Phát tín hiệu tới UI để chuyển đổi giữa màn hình Offline và Login.

  4.2 Module Quản lý DB (database/manager.py)
   * Mẫu thiết kế Singleton: Đảm bảo toàn bộ ứng dụng dùng chung một kết nối duy nhất.
   * Tính năng Auto-Schema: Tự động thực thi run_schema() khi kết nối thành công lần đầu, đảm bảo tính toàn vẹn dữ liệu mà không cần can thiệp thủ công.

  4.3 Module Giao diện (ui/)
   * StackedWidget: Sử dụng để chuyển đổi mượt mà giữa các màn hình mà không cần mở nhiều cửa sổ.
   * TestSessionWidget: Quản lý bộ đếm giờ (QTimer) và logic tính điểm dựa trên lựa chọn của người dùng.

  ---

  5. Luồng dữ liệu chính (Data Flow)

   1. Khởi động: main.py chạy -> Khởi tạo ServerStatusMonitor.
   2. Kiểm tra kết nối:
       * Monitor kiểm tra Ngrok -> Lấy IP/Port -> Kết nối MySQL.
       * Nếu thành công: status_changed(True) -> Hiện màn hình Đăng nhập.
       * Nếu thất bại: Hiện màn hình Offline.
   3. Xác thực: Người dùng nhập thông tin -> Gửi tới DatabaseManager -> So sánh mã băm Bcrypt.
   4. Làm bài thi: Lấy câu hỏi ngẫu nhiên từ DB -> Người dùng chọn đáp án -> Tính điểm -> Lưu vào bảng test_results.

  ---

  6. Các tính năng bảo mật & Tối ưu
   * Bảo mật mật khẩu: Không bao giờ lưu mật khẩu dạng văn bản thuần túy. Luôn sử dụng bcrypt.
   * Tự phục hồi (Self-healing): Nếu Tunnel Ngrok bị ngắt và khởi động lại với Port mới, ứng dụng sẽ tự động phát hiện và cập nhật cấu hình mà không cần khởi động lại App.
   * Xử lý bất đồng bộ: Sử dụng QTimer để kiểm tra kết nối ngầm, tránh gây treo giao diện (UI Freeze).

  ---

  7. Kết luận
  Thiết kế này tập trung vào tính tiện dụng (UX) và tự động hóa (Automation). Bằng cách loại bỏ các bước cấu hình thủ công phức tạp, ứng dụng trở nên thân thiện hơn với người
  dùng cuối trong khi vẫn đảm bảo khả năng quản lý dữ liệu mạnh mẽ của một hệ thống trực tuyến.