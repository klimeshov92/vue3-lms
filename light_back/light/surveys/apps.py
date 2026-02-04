from django.apps import AppConfig


class SurveysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'surveys'
    # Изменение имени приложения.
    verbose_name = 'Опрос'
    # Подключаем сигналы.
    def ready(self):
        import surveys.signals

