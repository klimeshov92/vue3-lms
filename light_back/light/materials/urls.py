
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'materials'

# Роутер.
router = DefaultRouter()

router.register(r'materials', MaterialViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('material_content/<int:task_id>/', material_content, name='material_content'),
   path('material_review/<int:task_id>/', material_review, name='material_review'),
]
