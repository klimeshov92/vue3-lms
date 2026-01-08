from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
    # Изменение имени приложения.
    verbose_name = 'Комментарии'
    # Подключаем сигналы.
    def ready(self):
        import comments.signals