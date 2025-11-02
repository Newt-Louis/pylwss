import sys
from PySide6 import QtWidgets
from ui.windows.inherit_business_interface.MainAppWindow import MainAppWindow
from core.database.database_setup import run_migrations
from core.services.SynchronizationService import run_all_startup_syncs
from core.manager import DirectoryWatcher
from core.manager.DashboardSession import DashboardSession

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainAppWindow()
    run_migrations()
    run_all_startup_syncs()
    print("Đồng bộ hóa hoàn tất.")
    DirectoryWatcher.start_watching()
    DashboardSession()
    window.show()
    app.aboutToQuit.connect(DirectoryWatcher.stop_watching())
    sys.exit(app.exec())