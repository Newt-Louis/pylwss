from PySide6.QtCore import QObject, Signal

class EventBus(QObject):
    webserver_saved = Signal(dict)
    database_saved = Signal(dict)
    language_saved = Signal(dict)
    network_saved = Signal(dict)
    tools_saved = Signal(dict)
    log_received = Signal(str)
    service_status_changed = Signal(dict)
    app_exit = Signal()

event_bus = EventBus()