from core.database.model import LanguageSetting
from core.manager.EventBus import EventBus
from core.manager import DirectoryWatcher
from core.services import SynchronizationService
from core.repository import LanguageRepository, WebserverRepository


class LanguageCoreService:
    def __init__(self):
        self.language_repository = LanguageRepository
        self.webserver_repository = WebserverRepository

    def load_settings(self) -> list[LanguageSetting] | None:
        print(f"Language: Đang tải cấu hình...")
        try:
            settings_data = self.language_repository.get_all_languages_settings()
            return None if settings_data is {} else settings_data
        except:
            raise

    def load_all_language_versions(self):
        try:
            languages_version_data = self.language_repository.get_all_language_versions()
            return None if languages_version_data is {} else languages_version_data
        except:
            raise

    def save_settings(self,data_to_save: dict) -> bool:
            # data_to_save = {
            #     "language": current_language_selected,
            #     "selected_version": selected_version,
            #     "root_folder": root_folder,
            #     "is_ssl_enabled": is_ssl_enabled,
            #     "is_chosen": is_chosen,
            #     "ssl_port": ssl_port,
            # }
        try:
            setting_model = LanguageSetting(**data_to_save)

            if not self.language_repository.disable_all_languages():
                raise Exception

            success = self.language_repository.update_language_settings(setting_model)

            if success:
                print("Lưu ngôn ngữ thành công")
                EventBus.language_saved.emit(setting_model.__dict__)
                schedule_callback_function = lambda: SynchronizationService.sync_language_projects(
                    setting_model.language,
                    setting_model.root_folder
                )
                DirectoryWatcher.add_or_update_dynamic_watch('projects_root_directory',setting_model.root_folder,schedule_callback_function)

            if data_to_save["ssl_port"] is not None:
                self.webserver_repository.update_ssl_port(data_to_save["ssl_port"])

            return success
        except Exception as e:
            raise e