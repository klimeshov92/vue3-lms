
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'topics'

# Роутер.
router = DefaultRouter()

router.register(r'topics', TopicViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('topics/<int:topic_id>/comments/', topic_comments, name='topic_comments'),
   path('comments/create/', comment_create, name='comment_create'),
   path('comments/<int:comment_id>/', comment, name='comment'),
   path('comments/<int:comment_id>/update/', comment_update, name='comment_update'),
   path('comments/<int:comment_id>/delete/', comment_delete, name='comment_delete'),
]
