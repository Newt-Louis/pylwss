import sys, os

def run_main_ui_application():
    try:
        from PySide6 import QtWidgets
        from ui.windows.inherit_business_interface.MainAppWindow import MainAppWindow
        from core.database.database_setup import run_migrations
        from core.services.SynchronizationService import run_all_startup_syncs
        from core.manager import DirectoryWatcher
        from core.manager.DashboardSession import DashboardSession
        from core.manager.PortManager import PortManager
        from core.config import config
    except ImportError as e:
        print(f"LỖI: Không thể import các module cần thiết: {e}")
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    window = MainAppWindow()

    run_migrations()
    run_all_startup_syncs()
    print("Đồng bộ hóa hoàn tất.")

    DirectoryWatcher.start_watching()
    DashboardSession()
    PortManager(config_path=os.path.join(config.APP_DATA_PORTS, 'ports.json'), start_port=8000, end_port=8999)

    window.show()

    app.aboutToQuit.connect(DirectoryWatcher.stop_watching)

    sys.exit(app.exec())

if __name__ == "__main__":
    if '--sync-hosts' in sys.argv:
        try:
            from core.services.HostFileService import sync_hosts_file

            sync_hosts_file()
            print("Đồng bộ hosts thành công.")

        except ImportError:
            print("LỖI: Không tìm thấy HostFileService.")
        except PermissionError as e:
            print(f"LỖI: Dù đã gọi UAC nhưng vẫn không có quyền. {e}")
            with open("admin_task.log", "w") as f:
                f.write(str(e))
        except Exception as e:
            print(f"LỖI: Tác vụ Admin thất bại: {e}")
            with open("admin_task.log", "w") as f:
                f.write(str(e))
        finally:
            sys.exit()
    else:
        run_main_ui_application()