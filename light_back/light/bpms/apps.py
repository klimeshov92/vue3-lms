from django.apps import AppConfig


class BpmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bpms'
    # Изменение имени приложения.
    verbose_name = 'Система управления'
    # Подключаем сигналы.
    def ready(self):
        import bpms.signals
