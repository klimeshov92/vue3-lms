from guardian.utils import get_anonymous_user
from rest_framework.permissions import BasePermission
from guardian.shortcuts import get_objects_for_user
import logging

logger = logging.getLogger('project')

from guardian.utils import get_anonymous_user
from guardian.shortcuts import get_objects_for_user
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger('project')


ACTION_PERMISSION_MAP = {
    'list': 'view',
    'retrieve': 'view',
    'create': 'add',
    'update': 'change',
    'partial_update': 'change',
    'destroy': 'delete',
}


class ObjectPermission(BasePermission):

    def get_user(self, request):
        if not request.user.is_authenticated:
            return get_anonymous_user()
        return request.user

    def has_permission(self, request, view):
        user = self.get_user(request)
        action = view.action

        model = getattr(view.queryset, 'model', None)
        if not model:
            logger.debug("Нет queryset.model — доступ разрешён")
            return True

        permission_codename = self.get_permission_codename(action, model)
        logger.debug(
            f"Проверка прав: user={user}, action={action}, permission={permission_codename}"
        )

        # Если для action не требуется permission
        if not permission_codename:
            return True

        # Глобальное разрешение
        if user.has_perm(permission_codename):
            logger.debug(f"Есть глобальное разрешение {permission_codename}")
            return True

        # LIST — объектные разрешения
        if action == 'list':
            try:
                qs = get_objects_for_user(user, permission_codename)
            except (Permission.DoesNotExist, ContentType.DoesNotExist):
                logger.warning(f"Permission {permission_codename} не существует")
                return False

            if qs.exists():
                view.queryset = qs
                logger.debug("Есть объектные разрешения для list")
                return True

        # Остальные — проверим объект
        if action in ['retrieve', 'update', 'partial_update', 'destroy']:
            obj = view.get_object()
            return self.has_object_permission(request, view, obj)

        logger.warning("Доступ запрещён")
        return False

    def has_object_permission(self, request, view, obj):
        user = self.get_user(request)
        action = view.action
        model = obj.__class__

        permission_codename = self.get_permission_codename(action, model)

        if not permission_codename:
            return True

        if user.has_perm(permission_codename):
            logger.debug(f"Есть глобальное разрешение {permission_codename}")
            return True

        try:
            if user.has_perm(permission_codename, obj):
                logger.debug(f"Есть объектное разрешение {permission_codename}")
                return True
        except (Permission.DoesNotExist, ContentType.DoesNotExist):
            logger.warning(f"Permission {permission_codename} не существует")
            return False

        logger.warning("Доступ запрещён на уровне объекта")
        return False

    def get_permission_codename(self, action, model):
        perm_action = ACTION_PERMISSION_MAP.get(action)
        if not perm_action:
            logger.debug(f"Action '{action}' не требует permission")
            return None

        ct = ContentType.objects.get_for_model(model)

        perm = Permission.objects.filter(
            content_type=ct,
            codename__startswith=f'{perm_action}_'
        ).first()

        if not perm:
            logger.warning(
                f"Permission '{perm_action}_*' для модели {model.__name__} не найден"
            )
            return None

        return f'{ct.app_label}.{perm.codename}'


class OldObjectPermission(BasePermission):

    def get_user(self, request):
        if not request.user.is_authenticated:
            return get_anonymous_user()
        return request.user

    def has_permission(self, request, view):
        user = self.get_user(request)
        action = view.action
        model_name = view.queryset.model._meta.model_name
        app_label = view.queryset.model._meta.app_label
        permission_codename = self.get_permission_codename(action, model_name, app_label)

        logger.debug(f"Текущий пользователь: {user}, authenticated: {user.is_authenticated}")
        logger.debug(f"Запрос: {request.method} {request.path}")
        logger.debug(f"Проверка прав для действия '{view.action}' с кодом разрешения '{permission_codename}'")

        if user.has_perm(permission_codename):
            logger.debug(f"Пользователь '{user}' имеет глобальное разрешение '{permission_codename}'")
            return True
        else:
            logger.debug(f"Пользователь '{user}' НЕ имеет глобальное разрешение '{permission_codename}'")

        if action == 'list':
            filtered_queryset = get_objects_for_user(user, permission_codename)
            if filtered_queryset.exists():
                view.queryset = filtered_queryset
                logger.debug(f"Пользователь '{user}' имеет объектные разрешения для объектов: {view.queryset}")
                return True

        if action in ['retrieve', 'partial_update', 'update', 'destroy']:
            obj = view.get_object()
            if self.has_object_permission(request, view, obj):
                return True

        logger.warning(f"Доступ запрещён функцией has_permission для пользователя '{user}'")
        return False

    def has_object_permission(self, request, view, obj):
        user = self.get_user(request)
        action = view.action
        model_name = view.queryset.model._meta.model_name
        app_label = view.queryset.model._meta.app_label
        permission_codename = self.get_permission_codename(action, model_name, app_label)

        if user.has_perm(permission_codename):
            logger.debug(f"Пользователь '{user}' имеет глобальное разрешение '{permission_codename}'")
            return True
        else:
            logger.debug(f"Пользователь '{user}' НЕ имеет глобальное разрешение '{permission_codename}'")

        if user.has_perm(permission_codename, obj):
            logger.debug(f"Пользователь '{user}' имеет объектное разрешение '{permission_codename}' для объекта '{obj}'")
            return True
        else:
            logger.debug(f"Пользователь '{user}' НЕ имеет объектное разрешение '{permission_codename}' для объекта '{obj}'")

        logger.warning(f"Доступ запрещён функцией has_object_permission для пользователя '{user}'")
        return False

    def get_permission_codename(self, action, model_name, app_label):
        if action in ['list', 'retrieve']:
            return f'{app_label}.view_{model_name}'
        elif action == 'self_create':
            return f'{app_label}.self_{model_name}'
        elif action == 'create':
            return f'{app_label}.add_{model_name}'
        elif action in ['update', 'partial_update']:
            return f'{app_label}.change_{model_name}'
        elif action == 'destroy':
            return f'{app_label}.delete_{model_name}'
        return ''
