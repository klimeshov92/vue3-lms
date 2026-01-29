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
    """
    Универсальная проверка прав:
    - глобальные права
    - объектные права (через django-guardian)
    - поддержка permission_map во ViewSet
    """

    def get_user(self, request):
        """
        Возвращаем пользователя запроса.
        Если не аутентифицирован — anonymous_user (guardian).
        """
        user = request.user if request.user.is_authenticated else get_anonymous_user()
        logger.debug(
            f"[PERM] Пользователь определён: {user} | authenticated={user.is_authenticated}"
        )
        return user

    def has_permission(self, request, view):
        """
        Проверка прав НА УРОВНЕ ЗАПРОСА (list, retrieve, create и т.д.)
        """
        user = self.get_user(request)
        action = view.action

        logger.debug(
            f"[PERM] has_permission: user={user}, action={action}, view={view.__class__.__name__}"
        )

        # ============================================================
        # 1. ЯВНО ЗАДАННЫЕ ПРАВА ИЗ ViewSet.permission_map
        # ============================================================
        if hasattr(view, 'permission_map') and action in view.permission_map:
            perm = view.permission_map[action]

            logger.debug(
                f"[PERM_MAP] Проверка permission_map: action={action}, permission={perm}"
            )

            # --- 1.1 Глобальное право ---
            has_global = user.has_perm(perm)
            logger.debug(
                f"[PERM_MAP] Глобальное право {perm}: {has_global}"
            )

            if has_global:
                logger.debug("[PERM_MAP] Доступ разрешён по глобальному праву")
                return True

            # --- 1.2 LIST → объектные права ---
            if action == 'list':
                qs = get_objects_for_user(user, perm)
                logger.debug(
                    f"[PERM_MAP] Объектные права (list): найдено объектов = {qs.count()}"
                )

                if qs.exists():
                    view.queryset = qs
                    logger.debug("[PERM_MAP] Доступ разрешён по объектным правам (list)")
                    return True

                logger.warning("[PERM_MAP] Доступ запрещён (list)")
                return False

            # --- 1.3 retrieve / update / delete → ПРОВЕРКА ОБЪЕКТА ---
            if action in ('retrieve', 'update', 'partial_update', 'destroy'):
                logger.debug(
                    "[PERM_MAP] Переходим к has_object_permission для объекта"
                )
                return self.has_object_permission(
                    request, view, view.get_object()
                )

            logger.warning("[PERM_MAP] Доступ запрещён (неподдерживаемое действие)")
            return False

        # ============================================================
        # 2. FALLBACK — АВТОМАТИЧЕСКИЕ ПРАВА ПО МОДЕЛИ
        # ============================================================
        model = getattr(view.queryset, 'model', None)
        logger.debug(f"[PERM_MODEL] Модель определена: {model}")

        if not model:
            logger.debug("[PERM_MODEL] Модель не найдена → доступ разрешён")
            return True

        perm = self._get_permission_codename(action, model)

        logger.debug(
            f"[PERM_MODEL] Проверка прав: action={action}, permission={perm}"
        )

        if not perm:
            logger.debug("[PERM_MODEL] Для действия не требуется permission")
            return True

        # --- 2.1 Глобальное право ---
        has_global = user.has_perm(perm)
        logger.debug(
            f"[PERM_MODEL] Глобальное право {perm}: {has_global}"
        )

        if has_global:
            logger.debug("[PERM_MODEL] Доступ разрешён по глобальному праву")
            return True

        # --- 2.2 LIST → объектные права ---
        if action == 'list':
            qs = get_objects_for_user(user, perm)
            logger.debug(
                f"[PERM_MODEL] Объектные права (list): найдено объектов = {qs.count()}"
            )

            if qs.exists():
                view.queryset = qs
                logger.debug("[PERM_MODEL] Доступ разрешён по объектным правам (list)")
                return True

        # --- 2.3 retrieve / update / delete → ПРОВЕРКА ОБЪЕКТА ---
        if action in ('retrieve', 'update', 'partial_update', 'destroy'):
            logger.debug(
                "[PERM_MODEL] Переходим к has_object_permission для объекта"
            )
            return self.has_object_permission(
                request, view, view.get_object()
            )

        logger.warning("[PERM_MODEL] Доступ запрещён")
        return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка ПРАВ НА КОНКРЕТНЫЙ ОБЪЕКТ
        """
        user = self.get_user(request)
        action = view.action
        model = obj.__class__

        logger.debug(
            f"[PERM_OBJ] Проверка объектных прав: user={user}, action={action}, obj_id={obj.id}"
        )

        perm = self._get_permission_codename(action, model)
        logger.debug(f"[PERM_OBJ] Определён permission: {perm}")

        if not perm:
            logger.debug("[PERM_OBJ] Permission не требуется → доступ разрешён")
            return True

        # --- Глобальное право ---
        has_global = user.has_perm(perm)
        logger.debug(
            f"[PERM_OBJ] Глобальное право {perm}: {has_global}"
        )

        if has_global:
            logger.debug("[PERM_OBJ] Доступ разрешён по глобальному праву")
            return True

        # --- Объектное право ---
        try:
            has_object = user.has_perm(perm, obj)
            logger.debug(
                f"[PERM_OBJ] Объектное право {perm} для obj_id={obj.id}: {has_object}"
            )
            return has_object
        except (Permission.DoesNotExist, ContentType.DoesNotExist) as e:
            logger.error(
                f"[PERM_OBJ] Ошибка проверки объектного права: {e}"
            )
            return False

    def _get_permission_codename(self, action, model):
        """
        Формирование permission вида:
        app_label.view_model
        app_label.add_model
        и т.д.
        """
        perm_action = ACTION_PERMISSION_MAP.get(action)
        logger.debug(
            f"[PERM_CODE] action={action}, perm_action={perm_action}, model={model}"
        )

        if not perm_action:
            logger.debug("[PERM_CODE] Для действия нет permission")
            return None

        ct = ContentType.objects.get_for_model(model)
        codename = f'{perm_action}_{model._meta.model_name}'

        exists = Permission.objects.filter(
            content_type=ct,
            codename=codename
        ).exists()

        logger.debug(
            f"[PERM_CODE] Проверка существования permission: {ct.app_label}.{codename} → {exists}"
        )

        if not exists:
            logger.warning(
                f"[PERM_CODE] Permission не найден: {ct.app_label}.{codename}"
            )
            return None

        full_perm = f'{ct.app_label}.{codename}'
        logger.debug(
            f"[PERM_CODE] Итоговый permission: {full_perm}"
        )
        return full_perm


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
