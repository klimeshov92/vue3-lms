
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'chats'

# Роутер.
router = DefaultRouter()

router.register(r'chats', ChatViewSet)
# router.register(r'messages', MessageViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('chats/<int:room_name>/messages/', chat_messages, name='chat_messages'),
]
