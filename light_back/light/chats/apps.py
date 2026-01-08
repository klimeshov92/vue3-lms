from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'
    # Изменение имени приложения.
    verbose_name = 'Чаты'
    # Подключаем сигналы.
    def ready(self):
        import chats.signals
