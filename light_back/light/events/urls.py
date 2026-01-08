
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'events'

# Роутер.
router = DefaultRouter()

router.register(r'event_templates', EventTemplateViewSet)
router.register(r'event_slots', EventSlotViewSet)


# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('confirm_participation/<int:task_id>/', confirm_participation, name='confirm_participation'),
   path('event_slot_select/<int:task_id>/', event_slot_select, name='event_slot_select'),
]
