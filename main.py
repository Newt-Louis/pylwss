import sys, os
from core.utils.Helper import get_base_path

def run_main_ui_application():
    BASE_DIR = get_base_path()
    os.chdir(BASE_DIR)
    try:
        from PySide6 import QtWidgets
        from ui.windows.inherit_business_interface.MainAppWindow import MainAppWindow
        from core.database.database_setup import run_migrations
        from core.services.SynchronizationService import run_all_startup_syncs
        from core.manager import DirectoryWatcher
        from core.manager.DashboardSession import DashboardSession
        from core.manager.PortManager import PortManager
        from core.manager.EventBus import event_bus
        from core.config import config
        import ui.resources.icons_rc
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

    app.aboutToQuit.connect(lambda: on_app_exit(DirectoryWatcher,event_bus))

    sys.exit(app.exec())

def on_app_exit(watcher,event_bus):
    watcher.stop_watching()
    event_bus.app_exit.emit()

if __name__ == "__main__":
    if '--sync-hosts' in sys.argv:
        try:
            from core.services.HostFileService import sync_hosts_file

            sync_hosts_file()

        except ImportError:
            print("LỖI: Không tìm thấy HostFileService.")
        except PermissionError as e:
            with open("admin_task.log", "w") as f:
                f.write(str(e))
        except Exception as e:
            with open("admin_task.log", "w") as f:
                f.write(str(e))
        finally:
            sys.exit()
    else:
        run_main_ui_application()