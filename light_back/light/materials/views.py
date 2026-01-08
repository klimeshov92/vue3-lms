from django.shortcuts import render

# Create your views here.

from .models import *
from .filters import *
from .serializers import *
from bpms.serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from core.permissions import ObjectPermission
from guardian.utils import get_anonymous_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from django.http import FileResponse
import mimetypes
from rest_framework.decorators import action


import logging
logger = logging.getLogger('project')

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = MaterialFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return MaterialEditSerializer
        elif self.action == 'partial_update':
            return MaterialEditSerializer
        return MaterialSerializer

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
def material_content(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.material_result

        executor = result.task.executor == request.user
        close = result.status == 'failed' or result.status == 'canceled'

        if not executor or close:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        if request.method == 'GET':
            serializer = MaterialResultSerializer(result, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при просмотре материала по задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def material_review(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.material_result

        executor = result.task.executor == request.user
        close = result.status == 'completed' or result.status == 'failed' or result.status == 'canceled'

        if not executor or close:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        result.status = 'completed'
        result.save()
        return Response("Ознакомление выполнено", status=200)

    except Exception as e:
        logger.exception(f"Ошибка при ознакомлении с материалом задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)


