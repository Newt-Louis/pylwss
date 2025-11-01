import sqlite3, os
from core.config import config

DB_PATH = config.DB_PATH

def sync_root_directory_to_db(language:str, root_directory_path: str):
    try:
        projects = {
            name for name in os.listdir(root_directory_path)
            if os.path.isdir(os.path.join(root_directory_path, name))
        }
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy thư mục: {root_directory_path}")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Kiểm tra đồng bộ dữ liệu
            cursor.execute("SELECT * FROM projects WHERE language = ?", (language,))
            projects_in_db = [row for row in cursor.fetchall()]
            projects_in_db_names = {row['project_name'] for row in projects_in_db}
            projects_to_add = projects - projects_in_db_names
            projects_to_delete = projects_in_db_names - projects

            if not projects_to_add and not projects_to_delete:
                print(f"{language} Đã đồng bộ dự án, không thay đổi gì!")
                return

            if projects_to_delete:
                delete_tuples = [(name, language) for name in projects_to_delete]
                cursor.executemany("DELETE FROM projects WHERE project_name =?",delete_tuples)

            if projects_to_add:
                insert_list = []
                for name in projects_to_add:
                    full_path = os.path.join(root_directory_path, name)
                    normalized_path = os.path.normpath(full_path)
                    insert_list.append((
                        name,  # project_name
                        language,  # language
                        normalized_path  # project_path
                    ))

                cursor.executemany("INSERT INTO projects VALUES (?, ?, ?)", insert_list)
                print(f"{language} Đồng bộ hoàn tất")
    except sqlite3.Error as e:
        print("Có lỗi khi đồng bộ vào db: ",e)
