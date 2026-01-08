from django.apps import AppConfig


class TestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
    # Изменение имени приложения.
    verbose_name = 'Тест'
    # Подключаем сигналы.
    def ready(self):
        import tests.signals
