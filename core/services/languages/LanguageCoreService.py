from core.database.model import LanguageSetting
from core.manager.EventBus import event_bus
from core.manager import DirectoryWatcher
from core.services import SynchronizationService
from core.repository import LanguageRepository, WebserverRepository, ProjectRepository


class LanguageCoreService:
    def __init__(self):
        self.language_repository = LanguageRepository
        self.webserver_repository = WebserverRepository
        self.project_repository = ProjectRepository

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
        success = False
        try:
            setting_model = LanguageSetting(**data_to_save)

            # Kiểm tra nếu lưu lại ngôn ngữ đó thì xóa các dự án đang được lưu và cập nhật lại file .conf
            current_language_in_db = self.language_repository.get_current_language_setting()
            if current_language_in_db is None:
                pass
            elif current_language_in_db.language == setting_model.language:
                success = self.language_repository.update_language_settings(setting_model)
                self.project_repository.delete_specified_language_projects(setting_model.language)
            else:
                if not self.language_repository.disable_all_languages():
                    raise Exception
                success = self.language_repository.update_language_settings(setting_model)

            if success:
                event_bus.language_saved.emit(setting_model.model_dump())
                schedule_callback_function = lambda: SynchronizationService.sync_language_projects(
                    setting_model.language,
                    setting_model.root_folder
                )
                schedule_callback_function()
                DirectoryWatcher.add_or_update_dynamic_watch('projects_root_directory',setting_model.root_folder,schedule_callback_function)

            if data_to_save["ssl_port"] is not None:
                self.webserver_repository.update_ssl_port(data_to_save["ssl_port"])

            return success
        except Exception as e:
            print("Có lỗi khi lưu cấu hình language",e)
            raise e