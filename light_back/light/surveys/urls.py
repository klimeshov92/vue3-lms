
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'survey'

# Роутер.
router = DefaultRouter()

router.register(r'surveys', SurveyViewSet)
router.register(r'survey_sections', SurveySectionViewSet)
router.register(r'survey_section_questions', SurveySectionQuestionViewSet)
router.register(r'survey_questions', SurveyQuestionViewSet)
router.register(r'survey_answers', SurveyAnswerViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('survey_attempt/<int:task_id>/', survey_attempt, name='survey_attempt'),
   path('survey_attempt_open/<int:task_id>/', survey_attempt_open, name='survey_attempt_open'),
   path('survey_attempt_create/<int:task_id>/', survey_attempt_create, name='survey_attempt_create'),
   path('send_survey_answers/<int:survey_question_result_id>/', send_survey_answers, name='send_survey_answers'),
   path('survey_finish/<int:survey_attempt_id>/', survey_finish, name='survey_finish'),
]
