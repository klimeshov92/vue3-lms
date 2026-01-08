
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'news'

# Роутер.
router = DefaultRouter()

router.register(r'news', NewViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('new_content/<int:task_id>/', new_content, name='new_content'),
   path('new_review/<int:task_id>/', new_review, name='new_review'),
]
