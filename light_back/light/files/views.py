from django.shortcuts import render

# Create your views here.

from .models import *
from .filters import *
from .serializers import *
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

import logging
logger = logging.getLogger('project')

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = FileFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return FileEditSerializer
        elif self.action == 'partial_update':
            return FileEditSerializer
        return FileSerializer

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
def download_file(request, file_id):
    try:
        logger.debug(f"Запрос на скачивание файла. file_id: {file_id}")

        file = get_object_or_404(File, id=file_id)
        logger.debug(f"Файл найден в базе: {file.name}, путь: {file.upload_file.path}")

        user = request.user if request.user.is_authenticated else get_anonymous_user()
        logger.debug(f"Пользователь: {user} (аутентифицирован: {request.user.is_authenticated})")

        if not (user.has_perm('files.view_file') or user.has_perm('files.view_file', file)):
            logger.warning(f"Пользователь {user} не имеет прав на просмотр файла {file_id}")
            return Response({"error": "Нет доступа"}, status=403)

        file_path = file.upload_file.path
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден по пути: {file_path}")
            return Response({"error": "Файл не найден"}, status=404)

        filename = os.path.basename(file.upload_file.name)
        mime_type, _ = mimetypes.guess_type(file_path)
        logger.debug(f"Имя файла: {filename}")
        logger.debug(f"MIME-тип: {mime_type}")

        response = FileResponse(
            open(file_path, 'rb'),
            content_type=mime_type or 'application/octet-stream',
            as_attachment=True,
            filename=filename
        )
        logger.debug(f"Заголовок Content-Disposition: {response['Content-Disposition']}")
        logger.debug(f"Content-Type: {response['Content-Type']}")

        return response

    except Exception as e:
        logger.exception(f"Ошибка при скачивании файла ID={file_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)


