from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    # Изменение имени приложения.
    verbose_name = 'Новости'
    # Подключаем сигналы.
    def ready(self):
        import news.signals
