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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
import json
import random
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q

import logging
logger = logging.getLogger('project')

class EventTemplateViewSet(viewsets.ModelViewSet):
    queryset = EventTemplate.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = EventTemplateFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventTemplateEditSerializer
        elif self.action == 'partial_update':
            return EventTemplateEditSerializer
        return EventTemplateSerializer

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

class EventSlotViewSet(viewsets.ModelViewSet):
    queryset = EventSlot.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = EventSlotFilter
    ordering_fields = ['planned_start', 'planned_end']
    ordering = ['planned_start', 'planned_end']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventSlotEditSerializer
        elif self.action == 'partial_update':
            return EventSlotEditSerializer
        return EventSlotSerializer

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

@api_view(['PATCH'])
@permission_classes([AllowAny])
def confirm_participation(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.event_result

        if not task.event_slot:
            return Response({"error": "Нет слота для подтверждения участия"}, status=403)

        executor = result.task.executor == request.user
        if not (executor):
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        result.confirmed = not result.confirmed
        result.save()
        return Response({"confirmed": result.confirmed},status=200)

    except Exception as e:
        logger.exception(f"Ошибка при подтверждении участия по задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET','PATCH'])
@permission_classes([AllowAny])
def event_slot_select(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)

        slot_select = task.slot_select
        if not slot_select:
            return Response({"error": "Нельзя выбирать слот мероприятия"}, status=403)

        executor = task.executor == request.user
        if not executor:
            return Response({"error": "Нет прав на задачу"}, status=403)

        if request.method == 'GET':
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PATCH':

            event_slot_id = request.data.get('event_slot')
            if event_slot_id:
                event_slot = get_object_or_404(EventSlot, pk=event_slot_id)
                if not event_slot.registration:
                    return Response({"error": "Регистрация на слот еще не открыта"}, status=403)

            serializer = TaskEditSerializer(task, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception(f"Ошибка при выборе слота мероприятия в задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def mark_completion(request, task_id, status):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.event_result

        if not task.event_slot:
            return Response({"error": "Нет слота для подтверждения участия"}, status=403)

        executor = result.task.executor == request.user
        if not (executor):
            return Response({"error": "Нет прав на результат задачи"}, status=403)


        result.status = status
        result.save()
        return Response({"status": result.status},status=200)

    except Exception as e:
        logger.exception(f"Ошибка при отметке выполнения по задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)