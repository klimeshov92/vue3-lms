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

import logging
logger = logging.getLogger('project')

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = ChatFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatEditSerializer
        elif self.action == 'partial_update':
            return ChatEditSerializer
        return ChatSerializer

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
def chat_messages(request, room_name):
    try:
        # Забираем чат.
        chat = Chat.objects.filter(id=room_name).first()
        if not chat:
            return Response({'error': 'Чат не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверка прав.
        user = request.user
        permission_codename = 'chats.view_chat'
        prem = False

        if user.has_perm(permission_codename):
            logger.debug(f"Пользователь '{user}' имеет глобальное разрешение '{permission_codename}'")
            prem = True
        elif user.has_perm(permission_codename, chat):
            logger.debug(f"Пользователь {user} имеет объектное право {permission_codename} на чат {chat}")
            prem = True
        else:
            logger.debug(f"Пользователь {user} не имеет права {permission_codename} на чат {chat}")

        if not prem:
            return Response({'error': 'У вас нет доступа к этому чату'}, status=status.HTTP_403_FORBIDDEN)

        # Получаем все сообщения для чата.
        messages = Message.objects.filter(chat=chat).order_by('created')

        # Сериализация сообщений.
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Ошибка при загрузке сообщений чата: {e}")
        return Response({'error': 'Ошибка при загрузке сообщений чата', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

