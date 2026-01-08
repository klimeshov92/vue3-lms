
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'courses'

# Роутер.
router = DefaultRouter()

router.register(r'courses',CourseViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('download_scorm/<int:course_id>/', download_scorm, name='download_scorm'),
   path('scorm_content/<int:task_id>/', scorm_content, name='scorm_content'),
   path('scorm_initialize/', scorm_initialize, name='scorm_initialize'),
   path('scorm_finish/', scorm_finish, name='scorm_finish'),
   path('get_value/', scorm_get_value, name='scorm_get_value'),
   path('set_value/', scorm_set_value, name='scorm_set_value'),
   path('scorm_commit/', scorm_commit, name='scorm_commit'),
   path('get_last_error/', scorm_get_last_error, name='scorm_get_last_error'),
   path('get_error_string/', scorm_get_error_string, name='scorm_get_error_string'),
   path('get_diagnostic/', scorm_get_diagnostic, name='scorm_get_diagnostic'),
]
