# Импортируем настройки.
from django.conf import settings
# Импортируем модуль models.
from django.db import models
# Импортируем post_save из модуля signals. post_save - сигнал, который отправляется после сохранения объекта модели.
from django.db.models.signals import post_save, post_delete
# Импортируем receiver из модуля dispatch. receiver - функция-декоратор для подключения функций обработки сигналов.
from django.dispatch import receiver
# Импортируем ответ с ошибкой сервера.
from django.http import HttpResponseServerError
# Импортируем пользовательские модели из текущего приложения.
# Эти модели используются для создания связанных объектов в базе данных.
from .models import Organization, Subdivision, Position, Account, Placement, AccountsGroup, GroupGenerator, AccountObjectPermission, AccountsGroupObjectPermission
from bpms.models import Interaction, ControlElementEvent
from bpms.functions import process_events
# Импортируем функцию make_password из модуля auth.hashers. Используется для хеширования паролей.
from django.contrib.auth.hashers import make_password
# Импортируем функцию get_random_string из модуля utils.crypto.
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from datetime import date
from notifications.models import NotificationSettings
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign_perm

# Импортируем логи.
import logging
# Создаем логгер с именем 'project'.
logger = logging.getLogger('project')

@receiver(post_save, sender=Organization)
def organizations_post_save(sender, instance, created, **kwargs):
    try:
        # Устанавливаем имя группы для организации.
        group_name = f"Организация: [{instance.id}] {instance.legal_name}"

        # Если организация только что создана.
        if created:
            group, _ = AccountsGroup.objects.get_or_create(name=group_name, type='organization')
            instance.group = group  # Связываем созданную группу с организацией.
            instance.save()  # Сохраняем изменения в организации.
            logger.info(f"Для организации {instance.legal_name} создана группа: {instance.group}")
        # Если имя группы изменилось после обновления организации.
        elif instance.group.name != group_name:
            instance.group.name = group_name
            instance.group.save()  # Сохраняем изменения в группе.
            logger.info(f"Для организации {instance.legal_name} обновлена группа: {instance.group}")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала post_save для Organization: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_delete, sender=Organization)
def delete_organizations_groups(sender, instance, **kwargs):
    try:
        # Удаляем связанные группы.
        instance.group.delete()
        logger.info(f"Удаляется связанная с организацией {instance} группа сотрудников {instance.group}.")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала delete_organizations_groups для Organization: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save, sender=Subdivision)
def subdivisions_post_save(sender, instance, created, **kwargs):
    try:
        # Устанавливаем имя группы для подразделения.
        group_name = f"Подразделение: [{instance.id}] {instance.name}"

        # Если подразделение только что создано.
        if created:
            group, _ = AccountsGroup.objects.get_or_create(name=group_name, type='subdivision')
            instance.group = group  # Связываем созданную группу с подразделением.
            instance.save()  # Сохраняем изменения в подразделении.
            logger.info(f"Для подразделения {instance.name} создана группа: {instance.group}")
        # Если имя группы изменилось после обновления подразделения.
        elif instance.group.name != group_name:
            instance.group.name = group_name
            instance.group.save()  # Сохраняем изменения в группе.
            logger.info(f"Для подразделения {instance.name} обновлена группа: {instance.group}")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала post_save для Subdivision: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_delete, sender=Subdivision)
def delete_subdivisions_groups(sender, instance, **kwargs):
    try:

        # Удаляем связанные группы.
        instance.group.delete()
        logger.info(f"Удаляется связанная с подразделением {instance} группа сотрудников {instance.group}.")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала delete_subdivisions_groups для Subdivision: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save, sender=Position)
def positions_post_save(sender, instance, created, **kwargs):
    try:
        # Устанавливаем имя группы для должности.
        group_name = f"Должность: [{instance.id}] {instance.name}"

        # Если должность только что создана.
        if created:
            group, _ = AccountsGroup.objects.get_or_create(name=group_name, type='position')
            instance.group = group  # Связываем созданную группу с должностью.
            instance.save()  # Сохраняем изменения в должности.
            logger.info(f"Для должности {instance.name} создана группа: {instance.group}")
        # Если имя группы изменилось после обновления должности.
        elif instance.group.name != group_name:
            instance.group.name = group_name
            instance.group.save()  # Сохраняем изменения в группе.
            logger.info(f"Для должности {instance.name} обновлена группа: {instance.group}")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала post_save для Position: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_delete, sender=Position)
def delete_position_groups(sender, instance, **kwargs):
    try:

        # Удаляем связанные группы.
        instance.group.delete()
        logger.info(f"Удаляется связанная с должностью {instance} группа сотрудников {instance.group}.")

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала delete_position_groups для Position: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save, sender=Account)
def employees_post_save(sender, instance, created, **kwargs):
    try:
        # Пропускаем логику сигнала для суперпользователей.
        if instance.is_superuser:
            return

        # Действия для только что созданных сотрудников.
        if created:
            notification_settings, _ = NotificationSettings.objects.get_or_create(account=instance)
            logger.debug(f"Созданы настройки оповещений {notification_settings} для пользователя {instance}")

            first_interaction = Interaction.objects.create(
                object_type='account',
                account=instance,
            )
            logger.debug(f"Создано первое взаимодействие {first_interaction} для пользователя {instance}")

            events = ControlElementEvent.objects.filter(
                event_type='account_created',
            ).select_related('control_element')

            process_events(events, first_interaction)

            if not instance.self_registration:
                # Установка случайного пароля для новых сотрудников.
                random_password = get_random_string(length=8)
                instance.set_password(random_password)
                instance.save()

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала post_save для Account: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save, sender=Placement)
def placements_post_save(sender, instance, created, **kwargs):
    try:

        # Добавление в группы при создании назначения.
        if created:
            instance.position.subdivision.organization.group.user_set.add(instance.employee)
            instance.position.subdivision.group.user_set.add(instance.employee)
            instance.position.group.user_set.add(instance.employee)

        # Обработка изменения или окончания назначения.
        else:
            # Получение всех активных назначений пользователя.
            active_placements = Placement.objects.filter(
                employee=instance.employee,
                end_date__isnull=True
            ).exclude(id=instance.id)

            # Перебор групп связанных с подразделением, должностью и организацией связанных с instance.
            for group in [instance.position.group, instance.position.subdivision.group, instance.position.subdivision.organization.group]:

                # Проверка, существует ли группа и состоит ли в ней пользователь.
                if group and group.user_set.filter(pk=instance.employee.pk).exists():

                    # Далее нужно проверить, есть ли другие активные назначения у сотрудника в этой группе.
                    if not active_placements.filter(position__group=group).exists() \
                            and not active_placements.filter(position__subdivision__group=group).exists() \
                            and not active_placements.filter(position__subdivision__organization__group=group).exists():
                        group.user_set.remove(instance.employee)

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала post_save для Placement: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_delete, sender=Placement)
def placement_post_delete(sender, instance, **kwargs):
    try:

        # Получение всех активных назначений пользователя.
        active_placements = Placement.objects.filter(
            account=instance.account,
            end_date__isnull=True
        ).exclude(id=instance.id)

        # Перебор групп связанных с подразделением, должностью и организацией связанных с instance.
        for group in [instance.position.group, instance.position.subdivision.group, instance.position.subdivision.organization.group]:

            # Проверка, существует ли группа и состоит ли в ней пользователь.
            if group and group.user_set.filter(pk=instance.account.pk).exists():

                # Далее нужно проверить, есть ли другие активные назначения у сотрудника в этой группе.
                if not active_placements.filter(position__group=group).exists() \
                        and not active_placements.filter(position__subdivision__group=group).exists() \
                        and not active_placements.filter(position__subdivision__organization__group=group).exists():
                    group.user_set.remove(instance.account)

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала placement_post_delete для Placement: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save, sender=GroupGenerator)
def update_groups_users(sender, instance, **kwargs):
    try:

        # Забирае переменные.
        group = instance.group
        added_groups = instance.added_groups.all()
        added_users = instance.added_users.all()
        excluded_groups = instance.excluded_groups.all()
        excluded_users = instance.excluded_users.all()

        # Выводим информацию о связях многие-ко-многим
        if settings.DEBUG:
            logger.info(f"Добавленные группы: {added_groups}")
            logger.info(f"Добавленные пользователи: {added_users}")
            logger.info(f"Исключенные группы: {excluded_groups}")
            logger.info(f"Исключенные пользователи: {excluded_users}")

        # Получаем добавляемых пользователей.
        all_added_users = Account.objects.filter(groups__in=added_groups, is_active=True).distinct() | added_users.distinct()
        if settings.DEBUG:
            logger.info(f"Все добавляемые пользователи: {all_added_users}")

        # Получаем добавляемых пользователей.
        all_excluded_users = Account.objects.filter(groups__in=excluded_groups, is_active=True).distinct() | excluded_users.distinct()
        if settings.DEBUG:
            logger.info(f"Все исключаемые пользователи: {all_excluded_users}")

        # Итог
        final_users = all_added_users.exclude(id__in=all_excluded_users.values_list('id', flat=True))
        if settings.DEBUG:
            logger.info(f"Все пользователи: {final_users}")

        # Фильтруем по датам.
        if instance.days_worked_lte is not None:
            start_date_lte = datetime.now().date() - timedelta(days=instance.days_worked_lte)
            final_users = final_users.filter(placements__start_date__gte=start_date_lte)
            logger.info(f"Пользователи с датой приема после {start_date_lte}: {final_users}")
        if instance.days_worked_gte is not None:
            start_date_gte = datetime.now().date() - timedelta(days=instance.days_worked_gte)
            final_users = final_users.filter(placements__start_date__lte=start_date_gte)
            logger.info(f"Пользователи с датой приема до {start_date_gte}: {final_users}")

        # Назначаем оставшихся пользователей группе.
        group.user_set.set(final_users)

    # Логирование исключений, если они возникнут.
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала update_groups_users для GroupGenerator: {e}", exc_info=True)
        # Повторный вызов исключения в режиме отладки.
        if settings.DEBUG:
            raise

@receiver(post_save)
def assign_creator_object_permissions(sender, instance, created, **kwargs):

    EXCLUDED_MODELS = {
        # Управляющие элементы.
        "controlelementevent",
        "controlelementcondition",
        "controlelementaction",

        # Результаты задач.
        "taskresult",
        "planresult",
        "materialresult",
        "newresult",
        "courseresult",
        "eventresult",
        "testresult",
        "testattempt",
        "questionresult",
        "answerresult",

        # Очереди.
        "queueexecutor",
        "queuetask",

        # Тесты
        "testsection",
        "testsectionquestion",
        "question",
        "answer",
        "relevantpoint",

        # Права.
        "permission",
        "accountsgroupobjectpermission",
        "accountobjectpermission",
    }

    try:
        if not created:
            return

        model_name = sender._meta.model_name.lower()

        # Исключённые модели.
        if model_name in EXCLUDED_MODELS:
            logger.debug(f"Пропускаем {model_name}: модель в списке исключений.")
            return

        # Пропуск системных моделей.
        if sender._meta.app_label in ["admin", "auth", "sessions", "contenttypes"]:
            return

        # Нет создателя.
        if not hasattr(instance, "creator"):
            return

        creator = instance.creator
        if not creator:
            logger.debug(f"{model_name}: creator отсутствует, пропускаем.")
            return

        content_type = ContentType.objects.get_for_model(sender)

        # Просмотр.
        perm_view = f"view_{model_name}"
        has_view = content_type.permission_set.filter(codename=perm_view).exists()

        if has_view:
            assign_perm(perm_view, creator, instance)
            logger.info(
                f"Назначено право {perm_view} создателю {creator} на {sender.__name__} (id={instance.pk})"
            )
        else:
            logger.debug(f"{model_name}: разрешение {perm_view} отсутствует, пропускаем.")

        # Изменение.
        perm_change = f"change_{model_name}"
        has_change = content_type.permission_set.filter(codename=perm_change).exists()

        if has_change:
            assign_perm(perm_change, creator, instance)
            logger.info(
                f"Назначено право {perm_change} создателю {creator} на {sender.__name__} (id={instance.pk})"
            )
        else:
            logger.debug(f"{model_name}: разрешение {perm_change} отсутствует, пропускаем.")

        creator.permissions_version += 1
        creator.save(update_fields=['permissions_version'])
        logger.info(
            f"Версия прав пользователя {creator.id} увеличена до {creator.permissions_version}"
        )

    except Exception as e:
        logger.error(
            f"Ошибка в assign_creator_object_permissions для модели {sender.__name__}: {e}",
            exc_info=True
        )

@receiver(post_delete)
def cleanup_object_permissions_for_instance(sender, instance, **kwargs):

    # Не трогаем системные приложения.
    if sender._meta.app_label in (
        'auth',
        'contenttypes',
        'admin',
        'sessions',
    ):
        return

    # Не трогаем сами object-permissions (иначе рекурсия).
    if sender.__name__ in (
        'UserObjectPermission',
        'GroupObjectPermission',
        'AccountObjectPermission',
        'AccountsGroupObjectPermission',
    ):
        return

    logger.debug(
        f'Удаление объектных прав: '
        f'{sender._meta.app_label}.{sender.__name__} (pk={instance.pk})'
    )

    content_type = ContentType.objects.get_for_model(
        instance,
        for_concrete_model=False
    )
    object_pk = str(instance.pk)

    user_deleted, _ = AccountObjectPermission.objects.filter(
        content_type=content_type,
        object_pk=object_pk
    ).delete()

    group_deleted, _ = AccountsGroupObjectPermission.objects.filter(
        content_type=content_type,
        object_pk=object_pk
    ).delete()

    if user_deleted or group_deleted:
        logger.debug(
            f'Удалено:'
            f'Права пользователей={user_deleted}, '
            f'Права групп={group_deleted}'
        )
    else:
        logger.debug(
            f'Нет объектных прав'
        )

