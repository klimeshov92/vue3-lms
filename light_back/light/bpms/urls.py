
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'bpms'

# Роутер.
router = DefaultRouter()

router.register(r'interactions', InteractionViewSet)
router.register(r'task_templates', TaskTemplateViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task_template_assignments', TaskTemplateAssignmentViewSet)
router.register(r'queues', QueueViewSet)
router.register(r'queue_tasks', QueueTaskViewSet)
router.register(r'queue_executors', QueueExecutorViewSet)
router.register(r'control_elements', ControlElementViewSet)
router.register(r'control_element_events', ControlElementEventViewSet)
router.register(r'control_element_conditions', ControlElementConditionViewSet)
router.register(r'control_element_actions', ControlElementActionViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('task_result_update/<int:task_id>/', task_result_update, name='task_result_update'),
   path('plan_result_update/<int:task_id>/', plan_result_update, name='plan_result_update'),
   path('self_assignment/<int:task_template_id>/', self_assignment, name='self_assignment'),
   path('plan_result_update/<int:task_id>/', plan_result_update, name='plan_result_update'),
   path('analytics_task_template/', analytics_task_template, name='analytics_task_template'),
]
