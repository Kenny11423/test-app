import sys
import os
# Thêm thư mục hiện tại vào đường dẫn để chúng ta có thể nhập cơ sở dữ liệu
sys.path.append(os.getcwd())

from database.manager import db_manager
from core.question import Category

def setup_categories():
    # Vì tôi đang chạy cái này trên máy tính xách tay máy chủ, tôi sẽ sử dụng localhost
    # thay vì đường hầm Ngrok dành cho các máy tính xách tay khác.
    db_manager.connect("localhost", "dbeaver", "123456", "test_prep_db", 3306)
    
    new_categories = [
        ("Math", "Các bài tập Toán học"),
        ("English", "Tiếng Anh (Ngữ pháp & Từ vựng)"),
        ("History", "Lịch sử Việt Nam và Thế giới"),
        ("Physics", "Vật lý đại cương"),
        ("Chemistry", "Hóa học cơ bản")
    ]
    
    print("Updating categories...")
    for name, desc in new_categories:
        try:
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
