
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'tests'

# Роутер.
router = DefaultRouter()

router.register(r'tests', TestViewSet)
router.register(r'test_sections', TestSectionViewSet)
router.register(r'test_section_questions', TestSectionQuestionViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'relevant_points', RelevantPointViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('test_attempt/<int:task_id>/', test_attempt, name='test_attempt'),
   path('test_attempt_open/<int:task_id>/', test_attempt_open, name='test_attempt_open'),
   path('test_attempt_create/<int:task_id>/', test_attempt_create, name='test_attempt_create'),
   path('send_answers/<int:question_result_id>/', send_answers, name='send_answers'),
   path('test_finish/<int:test_attempt_id>/', test_finish, name='test_finish'),
]
