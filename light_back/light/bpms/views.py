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
from .filters import *
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from collections import Counter


import logging
logger = logging.getLogger('project')

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = InteractionFilter
    ordering_fields = ['id']
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionEditSerializer
        elif self.action == 'partial_update':
            return InteractionEditSerializer
        return InteractionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class TaskTemplateViewSet(viewsets.ModelViewSet):
    queryset = TaskTemplate.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = TaskTemplateFilter
    ordering_fields = ['plan__name', 'item', 'name']
    ordering = ['plan__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskTemplateEditSerializer
        elif self.action == 'partial_update':
            return TaskTemplateEditSerializer
        return TaskTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = TaskFilter
    ordering_fields = ['planned_end', 'plan__name', 'item', 'name']
    ordering = ['planned_end']

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskEditSerializer
        elif self.action == 'partial_update':
            return TaskEditSerializer
        return TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class TaskTemplateAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskTemplateAssignment.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = TaskTemplateAssignmentFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskTemplateAssignmentEditSerializer
        elif self.action == 'partial_update':
            return TaskTemplateAssignmentEditSerializer
        return TaskTemplateAssignmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = QueueFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return QueueEditSerializer
        elif self.action == 'partial_update':
            return QueueEditSerializer
        return QueueSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class QueueExecutorViewSet(viewsets.ModelViewSet):
    queryset = QueueExecutor.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    #filterset_class = QueueFilter
    ordering_fields = ['item']
    ordering = ['item']

    def get_serializer_class(self):
        if self.action == 'create':
            return QueueExecutorEditSerializer
        elif self.action == 'partial_update':
            return QueueExecutorEditSerializer
        return QueueExecutorSerializer

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

class QueueTaskViewSet(viewsets.ModelViewSet):
    queryset = QueueTask.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    #filterset_class = QueueFilter
    ordering_fields = ['item']
    ordering = ['item']

    def get_serializer_class(self):
        if self.action == 'create':
            return QueueTaskEditSerializer
        elif self.action == 'partial_update':
            return QueueTaskEditSerializer
        return QueueTaskSerializer

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


class ControlElementViewSet(viewsets.ModelViewSet):
    queryset = ControlElement.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = ControlElementFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ControlElementEditSerializer
        elif self.action == 'partial_update':
            return ControlElementEditSerializer
        return ControlElementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        self.request._request.GET = query_params
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

class ControlElementEventViewSet(viewsets.ModelViewSet):
    queryset = ControlElementEvent.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    #filterset_class = ControlElementFilter
    ordering_fields = ['id']
    ordering = ['id']

    permission_map = {
        'create': 'bpms.add_control_element',
        'retrieve': 'bpms.view_control_element',
        'update': 'bpms.change_control_element',
        'partial_update': 'bpms.change_control_element',
        'destroy': 'bpms.delete_control_element',
        'list': 'bpms.view_control_element',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_control_element =self._object.control_element
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            control_element = None
            if self.action == 'create':
                control_element_id = self.request.data.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action == 'list':
                control_element_id = self.request.query_params.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                control_element = getattr(self, '_related_control_element', None)

            if control_element and not self.request.user.has_perm(perm_codename, control_element):
                self.permission_denied(self.request, message='Недостаточно прав на управляющий элемент')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для управляющий элемента {control_element}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return ControlElementEventEditSerializer
        elif self.action == 'partial_update':
            return ControlElementEventEditSerializer
        return ControlElementEventSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class ControlElementConditionViewSet(viewsets.ModelViewSet):
    queryset = ControlElementCondition.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    #filterset_class = ControlElementFilter
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'bpms.add_control_element',
        'retrieve': 'bpms.view_control_element',
        'update': 'bpms.change_control_element',
        'partial_update': 'bpms.change_control_element',
        'destroy': 'bpms.delete_control_element',
        'list': 'bpms.view_control_element',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_control_element =self._object.control_element
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            control_element = None
            if self.action == 'create':
                control_element_id = self.request.data.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action == 'list':
                control_element_id = self.request.query_params.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                control_element = getattr(self, '_related_control_element', None)

            if control_element and not self.request.user.has_perm(perm_codename, control_element):
                self.permission_denied(self.request, message='Недостаточно прав на управляющий элемент')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для управляющий элемента {control_element}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return ControlElementConditionEditSerializer
        elif self.action == 'partial_update':
            return ControlElementConditionEditSerializer
        return ControlElementConditionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class ControlElementActionViewSet(viewsets.ModelViewSet):
    queryset = ControlElementAction.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    #filterset_class = ControlElementFilter
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'bpms.add_control_element',
        'retrieve': 'bpms.view_control_element',
        'update': 'bpms.change_control_element',
        'partial_update': 'bpms.change_control_element',
        'destroy': 'bpms.delete_control_element',
        'list': 'bpms.view_control_element',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_control_element =self._object.control_element
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            control_element = None
            if self.action == 'create':
                control_element_id = self.request.data.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action == 'list':
                control_element_id = self.request.query_params.get('control_element')
                if control_element_id:
                    control_element = ControlElement.objects.filter(pk=control_element_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                control_element = getattr(self, '_related_control_element', None)

            if control_element and not self.request.user.has_perm(perm_codename, control_element):
                self.permission_denied(self.request, message='Недостаточно прав на управляющий элемент')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для управляющий элемента {control_element}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return ControlElementActionEditSerializer
        elif self.action == 'partial_update':
            return ControlElementActionEditSerializer
        return ControlElementActionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

@api_view(['GET','PATCH'])
@permission_classes([AllowAny])
def task_result_update(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.task_result

        executor = result.task.executor == request.user
        co_executor = result.task.co_executors.filter(id=request.user.id).exists()
        controller = result.task.controllers.filter(id=request.user.id).exists()

        if not (executor or co_executor or controller):
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        if request.method == 'GET':
            serializer = TaskResultSerializer(result, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = TaskResultEditSerializer(result, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception(f"Ошибка при обновлении результата задачи ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET','PATCH'])
@permission_classes([AllowAny])
def plan_result_update(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        result = task.plan_result

        executor = result.task.executor == request.user
        co_executor = result.task.co_executors.filter(id=request.user.id).exists()
        controller = result.task.controllers.filter(id=request.user.id).exists()

        if not (executor or co_executor or controller):
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        if request.method == 'GET':
            serializer = PlanResultSerializer(result, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = PlanResultEditSerializer(result, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception(f"Ошибка при обновлении результата задачи ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def self_assignment(request, task_template_id):
    try:

        task_template = get_object_or_404(TaskTemplate, pk=task_template_id)
        task_type = task_template.task_type

        user = request.user
        if task_type == 'news_reading':
            permission_codename = 'news.view_new'
            has_permission = (
                    user.has_perm(permission_codename) or
                    user.has_perm(permission_codename, task_template.new)
            )
        if task_type == 'material_review':
            permission_codename = 'materials.view_material'
            has_permission = (
                    user.has_perm(permission_codename) or
                    user.has_perm(permission_codename, task_template.material)
            )
        if task_type == 'course_study':
            permission_codename = 'courses.view_course'
            has_permission = (
                    user.has_perm(permission_codename) or
                    user.has_perm(permission_codename, task_template.course)
            )
        if task_type == 'test_taking':
            permission_codename = 'tests.view_test'
            has_permission = (
                    user.has_perm(permission_codename) or
                    user.has_perm(permission_codename, task_template.test)
            )
        if task_type == 'event_participation':
            permission_codename = 'events.view_event_slot'
            has_permission = (
                    user.has_perm(permission_codename) or
                    user.has_perm(permission_codename, task_template.event_slot)
            )
        if not has_permission:
            logger.debug(f"Пользователь {user} не имеет права на объект шаблона задачи {task_template}")
            return Response({'error': 'У вас нет доступа на объект шаблона задачи'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'POST':
            self_assignment = TaskTemplateAssignment.objects.create(
                name=f'Самоназначение {task_template.name}',
                task_template=task_template,
                interaction_type='last',
                executor_type='selected',
                executor=user,
                planned_start=timezone.now(),
                self_assignment=True
            )

            task = Task.objects.filter(
                assignment=self_assignment,
            ).order_by('id').first()

            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при самоназначении шаблона задачи ID={task_template_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

def get_task_result(task):
    task_type_to_result = {
        'common_task': 'task_result',
        'plan_implementation': 'plan_result',
        'news_reading': 'new_result',
        'material_review': 'material_result',
        'course_study': 'course_result',
        'event_participation': 'event_result',
        'test_taking': 'test_result',
    }
    return getattr(task, task_type_to_result.get(task.task_type, ''), None)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analytics_task_template(request):
    try:
        user = request.user

        if not user.has_perm('bpms.view_analytics'):
            return Response({'error': 'Нет прав на аналитику'}, status=403)

        data = request.data

        task_template_id = data.get('task_template')
        if not task_template_id:
            return Response({'error': 'task_template_id обязателен'}, status=400)

        task_template_obj = get_object_or_404(TaskTemplate, pk=task_template_id)

        # --- базовый queryset ---
        task_template_tasks = Task.objects.filter(task_template=task_template_obj)

        # --- фильтры по датам ---
        if data.get('planned_start_gte'):
            task_template_tasks = task_template_tasks.filter(
                task_result__start_time__gte=data['planned_start_gte']
            )

        if data.get('planned_start_lte'):
            task_template_tasks = task_template_tasks.filter(
                task_result__start_time__lte=data['planned_start_lte']
            )

        if data.get('planned_end_gte'):
            task_template_tasks = task_template_tasks.filter(
                task_result__end_time__gte=data['planned_end_gte']
            )

        if data.get('planned_end_lte'):
            task_template_tasks = task_template_tasks.filter(
                task_result__end_time__lte=data['planned_end_lte']
            )

        # --- фильтр по исполнителю ---
        executor_type = data.get('executor_type', 'all')

        if executor_type == 'account':
            account_id = data.get('account')
            if not account_id:
                return Response({'error': 'account_id обязателен'}, status=400)
            task_template_tasks = task_template_tasks.filter(executor_id=account_id)

        elif executor_type == 'group':
            group_id = data.get('group')
            if not group_id:
                return Response({'error': 'executor_group_id обязателен'}, status=400)

            group = get_object_or_404(AccountsGroup, pk=group_id)
            task_template_tasks = task_template_tasks.filter(
                executor__in=group.user_set.all()
            )

        tasks_started = task_template_tasks.count()

        # --- сбор сырых результатов ---
        results = []

        for task in task_template_tasks.select_related(
                'task_result',
                'plan_result',
                'new_result',
                'material_result',
                'course_result',
                'event_result',
                'test_result',
        ):
            result = get_task_result(task)
            if result:
                results.append(result)

        # --- статусы ---
        status_counter = Counter(r.status for r in results)

        # --- outcomes ---
        outcomes = [r.outcome for r in results if r.outcome_id]
        outcomes_counter = Counter(o.id for o in outcomes)
        outcomes_data = {}
        for outcome_id, count in outcomes_counter.items():
            outcome_obj = next(o for o in outcomes if o.id == outcome_id)
            outcomes_data[outcome_id] = {
                'name': outcome_obj.name,
                'count': count,
            }

        # --- сериализация ---
        task_template_data = TaskTemplateSerializer(
            task_template_obj,
            context={'request': request}
        ).data

        tasks_data = TaskSerializer(
            task_template_tasks,
            many=True,
            context={'request': request}
        ).data

        # --- ответ ---
        return Response({
            'report': 'task_template',
            'task_template': task_template_data,
            'tasks': tasks_data,
            'statuses': {
                'waiting': status_counter.get('waiting', 0),
                'assigned': status_counter.get('assigned', 0),
                'in_progress': status_counter.get('in_progress', 0),
                'completed': status_counter.get('completed', 0),
                'failed': status_counter.get('failed', 0),
                'canceled': status_counter.get('canceled', 0),
            },
            'outcomes': outcomes_data,
            'tasks_started': tasks_started,
            'tasks_finished': (status_counter.get('completed', 0)) + (status_counter.get('failed', 0)),
        })

    except Exception as e:
        logger.exception('Ошибка аналитики по шаблону задачи')
        return Response(
            {'error': 'Ошибка сервера', 'details': str(e)},
            status=500
        )

