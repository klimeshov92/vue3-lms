from django.shortcuts import render

# Create your views here.

from .models import *
from .serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from core.permissions import ObjectPermission
from guardian.utils import get_anonymous_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404


class NotificationSettingsViewSet(viewsets.ModelViewSet):
    queryset = NotificationSettings.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    #filterset_class = MaterialFilter
    ordering_fields = ['id']
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationSettingsEditSerializer
        elif self.action == 'partial_update':
            return NotificationSettingsEditSerializer
        return NotificationSettingsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

@api_view(['GET'])
@permission_classes([AllowAny])
def account_task_notifications(request, account_id):
    try:
        # Забираем аккаунт.
        account = get_object_or_404(Account, pk=account_id)

        # Проверка прав.
        if account != request.user:
            logger.debug(f"Пользователь не имеет права на чужие настройки оповещений")
            return Response({'error': 'Нельзя изменять чужие настройки оповещений'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            # Читаем параметр last_id.
            last_id = request.query_params.get('last_id')
            # Получаем все оповещения
            notifications = TaskNotification.objects.filter(account=account).order_by('-created')
            if last_id is not None:
                try:
                    last_id_int = int(last_id)
                    notifications = notifications.filter(id__gt=last_id_int)
                    logger.debug(f"Загружаются только оповещения после ID: {last_id_int}")
                except ValueError:
                    logger.warning(f"Неверный формат last_id: {last_id}")
            # Сериализация сообщений.
            serializer = TaskNotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Ошибка при загрузке оповещений: {e}")
        return Response({'error': 'Ошибка при загрузке оповещений', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def task_notification_read(request, task_notification_id):
    try:
        task_notification = get_object_or_404(TaskNotification, pk=task_notification_id)
        executor = task_notification.task.executor

        if executor != request.user:
            logger.debug(f"Пользователь не имеет права на изменение чужих оповещений")
            return Response({'error': 'Нет прав на изменение оповещения'}, status=status.HTTP_403_FORBIDDEN)

        task_notification.read = True
        task_notification.save()
        return Response(
            {
                "message": "Ознакомление выполнено",
                "task_notification_read": task_notification.read
            },
            status=200
        )

    except Exception as e:
        logger.exception(f"Ошибка при ознакомлении с оповещением ID={task_notification}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)


