
# Create your views here.

from .models import *
from .serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from .permissions import ObjectPermission
from guardian.utils import get_anonymous_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .pagination import CustomPageNumberPagination
from .filters import *
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from rest_framework.views import APIView
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

import logging
logger = logging.getLogger('project')

@api_view(['GET'])
@permission_classes([AllowAny])
def check_token(request):
    auth = request.headers.get('Authorization', None)

    if not auth:
        return Response({"error": "Authorization header is missing."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Получаем токен из заголовка.
        # Предполагается, что заголовок имеет вид "Bearer <token>".
        token = auth.split(' ')[1]
        # Проверяем и декодируем токен.
        validated_token = JWTAuthentication().get_validated_token(token)

        # Если токен действителен, возвращаем успех.
        return Response({"message": "Token is valid."})
    except (TokenError, InvalidToken) as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['model']
    ordering = ['model']

    def get_serializer_class(self):
        return ContentTypeBaseSerializer

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

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = AccountFilter
    ordering_fields = ['last_name', 'username', 'email']
    ordering = ['last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountEditSerializer
        elif self.action == 'partial_update':
            return AccountEditSerializer
        return AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'user_permissions[]' in query_params:
            query_params.setlist('user_permissions', query_params.getlist('user_permissions[]'))
            query_params.pop('user_permissions[]', None)
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
        password = self.request.data.get('password')
        if password:
            object.set_password(password)
            object.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()
        password = self.request.data.get('password')
        if password:
            object.set_password(password)
            object.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = ClientFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientEditSerializer
        elif self.action == 'partial_update':
            return ClientEditSerializer
        return ClientSerializer

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

@api_view(['GET'])
@permission_classes([AllowAny])
def user_permissions(request):
    try:
        # Убедимся, что пользователь аутентифицирован
        user = request.user if request.user.is_authenticated else get_anonymous_user()

        logger.debug(f"Аутентифицированный пользователь: {user}")

        # Получаем глобальные разрешения
        global_permissions = sorted(list(user.get_all_permissions()))
        logger.debug(f"Глобальные разрешения: {global_permissions}")

        # Получаем все разрешения
        all_permissions = Permission.objects.exclude(content_type__app_label='sessions').order_by('codename')
        logger.debug(f"Все доступные разрешения: {all_permissions}")
        object_permissions = {}  # Словарь для объектных разрешений

        # Собираем объектные разрешения для конкретного пользователя
        for permission in all_permissions:
            permission_codename = f'{permission.content_type.app_label}.{permission.codename}'
            logger.debug(f"Проверяем объектные разрешения для: {permission_codename}")

            objects_for_permission = get_objects_for_user(user, permission_codename, accept_global_perms=False)
            logger.debug(f"Объекты для разрешения {permission_codename}: {objects_for_permission}")

            if objects_for_permission.exists():
                object_permissions[permission_codename] = [obj.id for obj in objects_for_permission]

        logger.debug(f"Объектные разрешения пользователя: {object_permissions}")

        # Возвращаем JSON с глобальными и объектными разрешениями
        return Response({
            'user_id': user.id,
            'global_permissions': global_permissions,  # Список для JSON
            'object_permissions': object_permissions  # Словарь с разрешениями объектов
        })

    except Exception as e:
        logger.error(f"Ошибка при проверке разрешений: {e}")
        return Response({'error': 'Ошибка при проверке разрешений', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return PermissionEditSerializer
        elif self.action == 'partial_update':
            return PermissionEditSerializer
        return PermissionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        exclude_codenames = [
            "add_logentry", "change_logentry", "view_logentry", "delete_logentry",
            "add_session", "change_session", "view_session", "delete_session",
            "change_userobjectpermission", "add_userobjectpermission", "view_userobjectpermission", "delete_userobjectpermission",
            "change_groupobjectpermission", "add_groupobjectpermission", "view_groupobjectpermission", "delete_groupobjectpermission",
            "change_contenttype", "add_contenttype", "view_contenttype", "delete_contenttype",
            "change_group", "delete_group", "add_group", "view_group"
        ]
        queryset = queryset.exclude(codename__in=exclude_codenames)
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

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = CategoryFilter
    ordering_fields = ['name', 'parent_category__name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryEditSerializer
        elif self.action == 'partial_update':
            return CategoryEditSerializer
        return CategorySerializer

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

# Вью сет группы.
class AccountsGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountsGroup.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = AccountGroupFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountsGroupEditSerializer
        elif self.action == 'partial_update':
            return AccountsGroupEditSerializer
        return AccountsGroupSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params.copy()
        if 'categories[]' in query_params:
            query_params.setlist('categories', query_params.getlist('categories[]'))
            query_params.pop('categories[]', None)
        if 'user_set[]' in query_params:
            query_params.setlist('user_set', query_params.getlist('user_set[]'))
            query_params.pop('user_set[]', None)
        if 'permissions[]' in query_params:
            query_params.setlist('permissions', query_params.getlist('permissions[]'))
            query_params.pop('permissions[]', None)
        self.request._request.GET = query_params
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет прав группы.
class AccountsGroupObjectPermissionViewSet(viewsets.ModelViewSet):
    queryset = AccountsGroupObjectPermission.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    ordering_fields = ['permission__name']
    ordering = ['permission__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountsGroupObjectPermissionEditSerializer
        return AccountsGroupObjectPermissionBaseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет прав аккаунта.
class AccountObjectPermissionViewSet(viewsets.ModelViewSet):
    queryset = AccountObjectPermission.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['permission__name']
    ordering = ['permission__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountObjectPermissionEditSerializer
        elif self.action == 'partial_update':
            return AccountObjectPermissionEditSerializer
        return AccountObjectPermissionBaseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет организации.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    filterset_class = OrganizationFilter
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['legal_name']
    ordering = ['legal_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrganizationEditSerializer
        elif self.action == 'partial_update':
            return OrganizationEditSerializer
        return OrganizationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет отдела.
class SubdivisionViewSet(viewsets.ModelViewSet):
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionBaseSerializer
    permission_classes = [AllowAny, ObjectPermission]
    filterset_class = SubdivisionFilter
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['name', 'organization__legal_name', 'parent_subdivision__name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return SubdivisionEditSerializer
        elif self.action == 'partial_update':
            return SubdivisionEditSerializer
        return SubdivisionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет должность.
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('name')
    serializer_class = PositionBaseSerializer
    permission_classes = [AllowAny, ObjectPermission]
    filterset_class = PositionFilter
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['name', 'subdivision__name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return PositionEditSerializer
        elif self.action == 'partial_update':
            return PositionEditSerializer
        return PositionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет назначения на должность.
class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    ordering_fields = ['position__name']
    ordering = ['position__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return PlacementEditSerializer
        elif self.action == 'partial_update':
            return PlacementEditSerializer
        return PlacementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

# Вью сет генератора групп.
class GroupGeneratorViewSet(viewsets.ModelViewSet):
    queryset = GroupGenerator.objects.all()
    serializer_class = GroupGeneratorBaseSerializer
    permission_classes = [AllowAny, ObjectPermission]
    ordering_fields = ['group__name']
    ordering = ['group__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return GroupGeneratorEditSerializer
        elif self.action == 'partial_update':
            return GroupGeneratorEditSerializer
        return GroupGeneratorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        if settings.DEBUG:
            logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        if settings.DEBUG:
            logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        if settings.DEBUG:
            logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()


@api_view(['GET'])
@permission_classes([AllowAny])
def users_permissions(request):
    try:

        user = request.user
        if user.has_perm('auth.view_permission'):
            logger.debug(f"Пользователь '{user}' имеет глобальное разрешение '{'auth.view_permission'}'")
        else:
            logger.debug(f"Пользователь '{user}' НЕ имеет глобальное разрешение '{'auth.view_permission'}'")
            return Response({"error": "Нет прав на просмотр прав"}, status=403)


        account = request.query_params.get("account")
        name = request.query_params.get("name")

        users_qs = Account.objects.all()
        if account:
            account = get_object_or_404(Account, pk=account)
            users_qs = users_qs.filter(pk=account.id)

        data = []

        for user in users_qs:

            # Глобальные прямые права
            if user.is_superuser:
                direct_perms = Permission.objects.all()
            else:
                direct_perms = Permission.objects.filter(user=user)

            group_perms = Permission.objects.filter(group__user=user)
            direct_object_perms = AccountObjectPermission.objects.filter(user=user)
            group_object_perms = AccountsGroupObjectPermission.objects.filter(group__user=user)

            if name:
                direct_perms = direct_perms.filter(name__icontains=name)
                group_perms = group_perms.filter(name__icontains=name)
                direct_object_perms = direct_object_perms.filter(permission__name__icontains=name)
                group_object_perms = group_object_perms.filter(permission__name__icontains=name)

            # формируем единый список прав
            for p in direct_perms:
                data.append({
                    "user": {"id": user.id, "username": user.username, "is_superuser": user.is_superuser},
                    "type": "direct",
                    "permission": {"id": p.id, "name": p.name},
                    "group": None,
                    "object_perm_id": None,
                    "object": None,
                    "content_type": None,
                })

            for p in group_perms:
                for g in p.group_set.all():
                    if user in g.user_set.all():
                        data.append({
                            "user": {"id": user.id, "username": user.username, "is_superuser": user.is_superuser},
                            "type": "group",
                            "permission": {"id": p.id, "name": p.name},
                            "group": {"id": g.id, "name": g.name},
                            "object_perm_id": None,
                            "object": None,
                            "content_type": None,
                        })

            for p in direct_object_perms:
                obj_instance = p.permission.content_type.model_class().objects.get(pk=p.object_pk)
                data.append({
                    "user": {"id": user.id, "username": user.username, "is_superuser": user.is_superuser},
                    "type": "object_direct",
                    "permission": {"id": p.permission.id, "name": p.permission.name},
                    "group": None,
                    "object_perm_id": p.id,
                    "object": {"id": obj_instance.pk, "str": str(obj_instance)},
                    "content_type": {
                        "id": p.permission.content_type.id,
                        "verbose_name": p.permission.content_type.model_class()._meta.verbose_name
                    },
                })

            for p in group_object_perms:
                obj_instance = p.permission.content_type.model_class().objects.get(pk=p.object_pk)
                data.append({
                    "user": {"id": user.id, "username": user.username, "is_superuser": user.is_superuser},
                    "type": "object_group",
                    "permission": {"id": p.permission.id, "name": p.permission.name},
                    "group": {"id": p.group.id, "name": p.group.name} if p.group else None,
                    "object_perm_id": p.id,
                    "object": {"id": obj_instance.pk, "str": str(obj_instance)},
                    "content_type": {
                        "id": p.permission.content_type.id,
                        "verbose_name": p.permission.content_type.model_class()._meta.verbose_name
                    },
                })

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(result_page)


    except Exception as e:
        logger.exception(f"Ошибка при получении прав пользователей")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET','PATCH'])
@permission_classes([AllowAny])
def cabinet(request):
    try:
        account = get_object_or_404(Account, pk=request.user.id)

        if request.method == 'GET':
            serializer = CabinetSerializer(account, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = CabinetEditSerializer(account, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.exception(f"Ошибка при получении или обновлении данных кабинета пользователя: {account.username}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

import requests
def verify_recaptcha(token):
    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token,
        },
        timeout=5
    )
    return r.json().get('success', False)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        legal_agree = serializer.validated_data['legal_agree']
        policy_agree = serializer.validated_data['policy_agree']
        frontend_url = request.data.get('frontend_url')
        protocol = 'https' if request.is_secure() else 'http'
        captcha = request.data.get('captcha')

        if legal_agree != True:
            return Response({'legal_agree': 'Согласие с пользовательским соглашением обязательно.'}, status=status.HTTP_400_BAD_REQUEST)

        if policy_agree != True:
            return Response({'policy_agree': 'Согласие с политикой конфиденциальности обязательно.'}, status=status.HTTP_400_BAD_REQUEST)

        if not captcha or not verify_recaptcha(captcha):
            return Response({'captcha': 'Подтвердите, что вы не робот'}, status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.filter(username=username).first()

        if user:
            if user.is_active:
                return Response({'username': 'Пользователь с таким именем уже зарегистрирован и активирован.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Обновляем данные для неактивного пользователя
                user.email = email
                user.set_password(password)
                user.save()
        else:
            # Создаем нового пользователя
            user = Account.objects.create_user(
                username=username,
                email=email,
                password=password,
                legal_agree=True,
                policy_agree=True,
                is_active=False,
                self_registration = True
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'frontend_url': frontend_url,
            'protocol': protocol,
            'uid': uid,
            'token': token,
        })

        email_message = EmailMessage(
            subject='Активация аккаунта',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

        return Response({'detail': 'Письмо с подтверждением отправлено на ваш email.'},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'activation': True, 'detail': 'Аккаунт успешно активирован!'}, status=status.HTTP_200_OK)
    else:
        return Response({'activation': False, 'detail': 'Неверная или просроченная ссылка активации.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    frontend_url = request.data.get('frontend_url')
    protocol = 'https' if request.is_secure() else 'http'

    if not username or not email:
        return Response({'detail': 'Необходимо указать имя пользователя и email.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Account.objects.get(username=username, email=email)
    except Account.DoesNotExist:
        return Response({'detail': 'Пользователь с такими данными не найден.'},
                        status=status.HTTP_404_NOT_FOUND)

    if not user.is_active:
        return Response({'detail': 'Аккаунт не активирован.'},
                        status=status.HTTP_400_BAD_REQUEST)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    message = render_to_string('registration/password_reset_email_custom.html', {
        'user': user,
        'frontend_url': frontend_url,
        'protocol': protocol,
        'uid': uid,
        'token': token,
    })

    email_message = EmailMessage(
        subject='Восстановление доступа',
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email_message.content_subtype = 'html'
    email_message.send(fail_silently=False)

    return Response({'detail': 'Письмо для восстановления пароля отправлено на ваш email.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def provide_access_user_view(request, id):

    account = get_object_or_404(Account, pk=id)
    logger.debug(f"Отправка письма для предоставления доступа аккаунту {account}")
    if not account.is_active:
        logger.debug(f"Аккаунт не активирован - отправки не будет")
        return Response({'detail': 'Аккаунт не активирован.'}, status=status.HTTP_400_BAD_REQUEST)
    if not account.email:
        logger.debug(f"У аккаунта нет почты - отправки не будет")
        return Response({'detail': 'К аккаунту не привязан email.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    permission_codename = 'core.change_account'
    has_permission = (
            user.has_perm(permission_codename) or
            user.has_perm(permission_codename, account)
    )
    if not has_permission:
        logger.debug(f"Пользователь {user} не имеет права на редактирование аккаунта {account}")
        return Response({'error': 'У вас нет прав на редактирование аккаунта'}, status=status.HTTP_403_FORBIDDEN)

    frontend_url = request.data.get('frontend_url')
    if not frontend_url:
        return Response({'detail': 'frontend_url обязателен'}, status=400)
    protocol = 'https' if request.is_secure() else 'http'
    uid = urlsafe_base64_encode(force_bytes(account.pk))
    token = default_token_generator.make_token(account)

    message = render_to_string('registration/provide_access_user.html', {
        'user': account,
        'frontend_url': frontend_url,
        'protocol': protocol,
        'uid': uid,
        'token': token,
    })
    email_message = EmailMessage(
        subject='Предоставление доступа',
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email],
    )
    email_message.content_subtype = 'html'
    email_message.send(fail_silently=False)
    return Response({'detail': 'Письмо для предоставления доступа отправлено на аккаунту.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def provide_access_group_view(request, id):

    group = get_object_or_404(AccountsGroup, pk=id)
    user = request.user
    has_permission = (
            user.has_perm('core.change_accounts_group') or
            user.has_perm('core.change_accounts_group', group)
    )
    if not has_permission:
        return Response(
            {'error': 'Нет прав на редактирование группы'},
            status=status.HTTP_403_FORBIDDEN
        )
    frontend_url = request.data.get('frontend_url')
    if not frontend_url:
        return Response({'detail': 'frontend_url обязателен'}, status=400)
    protocol = 'https' if request.is_secure() else 'http'

    accounts = group.user_set.all()
    for account in accounts:
        logger.debug(f"Отправка письма для предоставления доступа аккаунту {account}")
        if not account.is_active:
            logger.debug(f"Аккаунт не активирован - отправки не будет")
            continue
        if not account.email:
            logger.debug(f"У аккаунта нет почты - отправки не будет")
            continue
        uid = urlsafe_base64_encode(force_bytes(account.pk))
        token = default_token_generator.make_token(account)

        message = render_to_string('registration/provide_access_user.html', {
            'user': account,
            'frontend_url': frontend_url,
            'protocol': protocol,
            'uid': uid,
            'token': token,
        })
        email_message = EmailMessage(
            subject='Предоставление доступа',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[account.email],
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

        logger.debug(f"Письмо отправлено")

    return Response({'detail': 'Письма для предоставления доступа отправлено на аккаунтам.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if not user or not default_token_generator.check_token(user, token):
        return Response(
            {'success': False, 'detail': 'Неверная или просроченная ссылка сброса пароля.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    new_password = request.data.get('password')

    if not new_password:
        return Response(
            {'success': False, 'detail': 'Необходимо указать новый пароль.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.is_active = True
    user.save()

    return Response(
        {'success': True, 'detail': 'Пароль успешно изменён. Теперь вы можете войти в систему.'},
        status=status.HTTP_200_OK
    )

class HomePageViewSet(viewsets.ModelViewSet):
    queryset = HomePage.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['title']
    ordering = ['title']

    def get_serializer_class(self):
        if self.action == 'create':
            return HomePageEditSerializer
        elif self.action == 'partial_update':
            return HomePageEditSerializer
        return HomePageSerializer

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
def home_page_content(request):
    try:
        home_page = HomePage.objects.first()

        if home_page:
            serializer = HomePageSerializer(home_page, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"detail": "Главная страница ещё не создана."}, status=200)

    except Exception as e:
        logger.exception(f"Ошибка при главной страницы")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

class LegalPageViewSet(viewsets.ModelViewSet):
    queryset = LegalPage.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['title']
    ordering = ['title']

    def get_serializer_class(self):
        if self.action == 'create':
            return LegalPageEditSerializer
        elif self.action == 'partial_update':
            return LegalPageEditSerializer
        return LegalPageSerializer

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
def legal_page_content(request):
    try:
        legal_page = LegalPage.objects.first()

        if legal_page:
            serializer = LegalPageSerializer(legal_page, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"detail": "Главная страница ещё не создана."}, status=200)

    except Exception as e:
        logger.exception(f"Ошибка при главной страницы")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

class PolicyPageViewSet(viewsets.ModelViewSet):
    queryset = PolicyPage.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['title']
    ordering = ['title']

    def get_serializer_class(self):
        if self.action == 'create':
            return PolicyPageEditSerializer
        elif self.action == 'partial_update':
            return PolicyPageEditSerializer
        return PolicyPageSerializer

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
def policy_page_content(request):
    try:
        policy_page = PolicyPage.objects.first()

        if policy_page:
            serializer = PolicyPageSerializer(policy_page, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"detail": "Главная страница ещё не создана."}, status=200)

    except Exception as e:
        logger.exception(f"Ошибка при главной страницы")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)
