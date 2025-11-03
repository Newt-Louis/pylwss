import sqlite3, os
from core.config import config
from core.manager.PortManager import PortManager
from core.repository import WebserverRepository
from core.services import ConfigGeneratorService

DB_PATH = config.DB_PATH
PHP_FPM_PORT = 9000

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
        port_manager = PortManager()
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Kiểm tra đồng bộ dữ liệu
            cursor.execute("SELECT * FROM projects WHERE language = ?", (language,))
            projects_in_db = [row for row in cursor.fetchall()]
            projects_in_db_map = {row['project_name']: row["id"] for row in projects_in_db}
            projects_in_db_names = set(projects_in_db_map.keys())
            projects_to_add = projects - projects_in_db_names
            projects_to_delete = projects_in_db_names - projects

            if not projects_to_add and not projects_to_delete:
                print(f"{language} Đã đồng bộ dự án, không thay đổi gì!")
                return

            if projects_to_delete:
                delete_tuples = []
                for name in projects_to_delete:
                    delete_tuples.append((name, language))
                    if language != 'php':
                        port_manager.release_port(name)
                    ConfigGeneratorService.remove_config_for_project(conn, projects_in_db_map[name])
                cursor.executemany("DELETE FROM projects WHERE project_name = ? AND language = ?",delete_tuples)

            if projects_to_add:
                insert_list = []
                # gọi hàm lấy top level domain hiện tại
                webserver = WebserverRepository.get_current_webserver()

                # Nếu webserver chưa chọn (khi ứng dụng cài đặt mới)
                if webserver is None:
                    print("Lỗi cấu hình webserver khi đồng bộ thư mục dự án gốc! xem lại webserver_settings")
                    return

                for name in projects_to_add:
                    full_path = os.path.join(root_directory_path, name)
                    normalized_path = os.path.normpath(full_path)
                    domain = f"{name}{'.test' if webserver["tld_template"] is None else webserver["tld_template"]}"
                    app_port = None
                    if language == 'php':
                        app_port = PHP_FPM_PORT
                    else:
                        app_port = port_manager.get_next_available_port(name)

                    if app_port is None:
                        print("Bộ số lượng cổng đã sử dụng hết (tổng cộng 1000 cổng đã sử dụng hết)!")
                        continue

                    insert_list.append((
                        name,            # project_name
                        language,        # language
                        normalized_path, # project_path
                        app_port,         # Cổng của ứng dụng
                        domain
                    ))

                cursor.executemany("INSERT INTO projects (project_name,language,project_path,app_port,domain) VALUES (?, ?, ?, ?, ?)", insert_list)
                if insert_list:
                    added_project_names = [item[0] for item in insert_list]
                    placeholders = ','.join('?' for _ in added_project_names)
                    sql_get_new_ids = f"SELECT id FROM projects WHERE language = ? AND project_name IN ({placeholders})"
                    params = (language,) + tuple(added_project_names)
                    cursor.execute(sql_get_new_ids, params)
                    newly_added_rows = cursor.fetchall()
                    for row in newly_added_rows:
                        new_project_id = row['id']
                        ConfigGeneratorService.regenerate_config_for_project(conn, new_project_id)

                print(f"{language} Đồng bộ hoàn tất")
    except sqlite3.Error as e:
        print("Có lỗi khi đồng bộ vào db: ",e)