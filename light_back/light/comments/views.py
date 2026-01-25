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

import logging
logger = logging.getLogger('project')

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = TopicFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return TopicEditSerializer
        elif self.action == 'partial_update':
            return TopicEditSerializer
        return TopicSerializer

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
def topic_comments(request, topic_id):
    try:
        # Забираем чат.
        topic = get_object_or_404(Topic, pk=topic_id)

        # Проверка прав.
        user = request.user
        permission_codename = 'comments.view_topic'
        has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, topic)
        )

        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {topic}")
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            # Читаем параметр last_id.
            last_id = request.query_params.get('last_id')
            # Получаем все сообщения для чата
            comments = Comment.objects.filter(topic=topic).order_by('created')
            if last_id is not None:
                try:
                    last_id_int = int(last_id)
                    comments = comments.filter(id__gt=last_id_int)
                    logger.debug(f"Загружаются только сообщения после ID: {last_id_int}")
                except ValueError:
                    logger.warning(f"Неверный формат last_id: {last_id}")
            # Сериализация сообщений.
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Ошибка при загрузке сообщений чата: {e}")
        return Response({'error': 'Ошибка при загрузке сообщений чата', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def comment_create(request):
    try:
        topic_id = request.data.get('topic')
        if not topic_id:
            return Response({'error': 'Не передан topic'}, status=status.HTTP_400_BAD_REQUEST)

        topic = get_object_or_404(Topic, pk=topic_id)

        # Проверка прав.
        user = request.user
        permission_codename = 'comments.view_topic'
        has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, topic)
        )

        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {topic}")
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'POST':
            serializer = CommentEditSerializer(data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception("Ошибка при создании комментария")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def comment(request, comment_id):
    try:

        comment = get_object_or_404(Comment, pk=comment_id)
        topic = comment.topic

        if not topic:
            return Response({'error': 'Чат не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверка прав.
        user = request.user
        permission_codename = 'comments.view_topic'
        has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, topic)
        )

        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {topic}")
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при получении комментария ID={comment_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def comment_update(request, comment_id):
    try:

        comment = get_object_or_404(Comment, pk=comment_id)
        topic = comment.topic

        if not topic:
            return Response({'error': 'Чат не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверка прав.
        user = request.user
        permission_codename = 'comments.view_topic'
        has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, topic)
        )

        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {topic}")
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PATCH':
            serializer = CommentEditSerializer(comment, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception(f"Ошибка при обновлении комментария ID={comment_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def comment_delete(request, comment_id):
    try:
        comment = get_object_or_404(Comment, pk=comment_id)
        topic = comment.topic

        if not topic:
            return Response({'error': 'Чат не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверка прав.
        user = request.user
        permission_codename = 'comments.view_topic'
        has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, topic)
        )

        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {topic}")
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'DELETE':
            comment.delete()
            return Response({'status': 'Комментарий удалён'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        logger.exception(f"Ошибка при удалении комментария ID={comment_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)