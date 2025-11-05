from dependency_injector import containers, providers
from core.services import WebserverCoreService, LanguageCoreService, DashboardCoreService
from core.services.databases.DatabaseCoreService import DatabaseCoreService
from ui.windows.inherit_business_interface import WebserverServiceController, LanguagesServiceController, \
    DatabasesServiceController, ToolsServiceController, NetworkServiceController, WebserverPageController, \
    LanguagesPageController, DatabasesPageController, DashboardServiceController


class ServiceContainer(containers.DeclarativeContainer):
    DashboardServiceController = providers.Singleton(DashboardServiceController, dashboard_core_service=DashboardCoreService)
    WebserverServiceController = providers.Singleton(WebserverServiceController,webserver_core_service=WebserverCoreService)
    LanguagesServiceController = providers.Singleton(LanguagesServiceController, language_core_service=LanguageCoreService)
    DatabasesServiceController = providers.Singleton(DatabasesServiceController, database_core_service=DatabaseCoreService)
    # ToolsServiceController = providers.Singleton(ToolsServiceController, ToolCoreService)
    # NetworkServiceController = providers.Singleton(NetworkServiceController, NetworkCoreService)