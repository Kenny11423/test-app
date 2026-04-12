import sys
import os
# Thêm thư mục hiện tại vào đường dẫn để chúng ta có thể nhập cơ sở dữ liệu
sys.path.append(os.getcwd())

from database.manager import db_manager
from core.question import Category

def setup_categories():
    # Thử đọc db.txt để lấy cấu hình
    host, port, user, pwd, dbname = "localhost", 3306, "root", "", "test_prep_db"
    if os.path.exists("db.txt"):
        try:
            with open("db.txt", "r") as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) >= 5:
                    host, port, user, pwd, dbname = lines[0], int(lines[1]), lines[2], lines[3], lines[4]
        except:
            pass
            
    db_manager.connect(host, user, pwd, dbname, port)
    
    new_categories = [
        ("Math", "Các bài tập Toán học"),
        ("English", "Tiếng Anh (Ngữ pháp & Từ vựng)"),
        ("History", "Lịch sử Việt Nam và Thế giới"),
        ("Physics", "Vật lý đại cương"),
        ("Chemistry", "Hóa học cơ bản"),
        ("Biology", "Sinh học"),
        ("Geography", "Địa lý"),
        ("Informatics", "Tin học"),
        ("Civics", "Giáo dục công dân")
    ]
    
    print("Updating categories...")
    for name, desc in new_categories:
        try:
            # Kiểm tra xem đã tồn tại chưa (tùy chọn, Category.add có thể xử lý)
            Category.add(name, desc)
            print(f"Added: {name}")
        except Exception as e:
            print(f"Failed to add {name}: {e}")

    # Liệt kê tất cả các danh mục để xác minh
    cats = Category.get_all()
    print("\nCurrent Categories in Database:")
    for c in cats:
        print(f"- {c.name}: {c.description}")

if __name__ == "__main__":
    setup_categories()
