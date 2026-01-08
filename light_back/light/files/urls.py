
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'files'

# Роутер.
router = DefaultRouter()

router.register(r'files', FileViewSet)
# router.register(r'messages', MessageViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('download_file/<int:file_id>/', download_file, name='download_file'),
]
