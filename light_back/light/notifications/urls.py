
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'notifications'

# Роутер.
router = DefaultRouter()

router.register(r'notification_settings', NotificationSettingsViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('accounts/<int:account_id>/task_notifications/', account_task_notifications, name='account_task_notifications'),
   path('task_notifications/<int:task_notification_id>/read/', task_notification_read, name='task_notification_read'),
]
