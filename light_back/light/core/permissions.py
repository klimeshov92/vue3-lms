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
        return request.user if request.user.is_authenticated else get_anonymous_user()

    def has_permission(self, request, view):
        user = self.get_user(request)
        action = view.action

        # === 1. ЯВНОЕ permission от ViewSet ===
        if hasattr(view, 'permission_map') and action in view.permission_map:
            perm = view.permission_map[action]

            logger.debug(
                f"[PERM_MAP] user={user}, action={action}, perm={perm}"
            )

            if user.has_perm(perm):
                return True

            if action == 'list':
                try:
                    qs = get_objects_for_user(user, perm)
                except (Permission.DoesNotExist, ContentType.DoesNotExist):
                    return False

                if qs.exists():
                    view.queryset = qs
                    return True

            return False

        # === 2. FALLBACK — по модели ===
        model = getattr(view.queryset, 'model', None)
        if not model:
            return True

        perm = self._get_permission_codename(action, model)

        logger.debug(
            f"[PERM_MODEL] user={user}, action={action}, perm={perm}"
        )

        if not perm:
            return True

        if user.has_perm(perm):
            return True

        if action == 'list':
            try:
                qs = get_objects_for_user(user, perm)
            except (Permission.DoesNotExist, ContentType.DoesNotExist):
                return False

            if qs.exists():
                view.queryset = qs
                return True

        if action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return self.has_object_permission(request, view, view.get_object())

        return False

    def has_object_permission(self, request, view, obj):
        user = self.get_user(request)
        action = view.action
        model = obj.__class__

        perm = self._get_permission_codename(action, model)
        if not perm:
            return True

        if user.has_perm(perm):
            return True

        try:
            return user.has_perm(perm, obj)
        except (Permission.DoesNotExist, ContentType.DoesNotExist):
            return False

    def _get_permission_codename(self, action, model):
        perm_action = ACTION_PERMISSION_MAP.get(action)
        if not perm_action:
            return None

        ct = ContentType.objects.get_for_model(model)
        codename = f'{perm_action}_{model._meta.model_name}'

        if not Permission.objects.filter(content_type=ct, codename=codename).exists():
            return None

        return f'{ct.app_label}.{codename}'

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
