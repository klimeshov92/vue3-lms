from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'
    # Изменение имени приложения.
    verbose_name = 'Файлы'
    # Подключаем сигналы.
    def ready(self):
        import files.signals

