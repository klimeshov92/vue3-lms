from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    # Изменение имени приложения.
    verbose_name = 'Уведомления'
    # Подключаем сигналы.
    def ready(self):
        import notifications.signals

