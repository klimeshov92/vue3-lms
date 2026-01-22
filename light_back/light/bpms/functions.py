from .models import ControlElementCondition
from .models import ControlElementAction, Task, Interaction
from datetime import datetime, timedelta
from django.utils import timezone
from .models import *
from notifications.models import *
from guardian.shortcuts import assign_perm

import logging
logger = logging.getLogger('project')

def assignment_task_create(instance, executor, task_template, plan=None):

    if instance.interaction_type == 'selected':
        if not instance.interaction:
            logger.debug("Не выбрано взаимодействие для исполнителя.")
            return

    elif instance.interaction_type == 'last':
        last_interaction = Interaction.objects.filter(
            account=executor
        ).order_by('-created').first()

        if last_interaction:
            instance.interaction = last_interaction
            logger.debug(
                f"Используем последнее взаимодействие с исполнителем {executor} для задачи {task_template.name}")
        else:
            instance.interaction = Interaction.objects.create(
                object_type='account',
                account=executor,
            )
            logger.debug(f"Создаём новое взаимодействие с исполнителем {executor} для задачи {task_template.name}")

    elif instance.interaction_type == 'new':
        instance.interaction = Interaction.objects.create(
            object_type='account',
            account=executor,
        )
        logger.debug(f"Создаём новое взаимодействие с исполнителем {executor} для задачи {task_template.name}")

    existing_task = Task.objects.filter(
        interaction=instance.interaction,
        task_template=task_template
    ).first()

    if existing_task:
        logger.debug(f"Задача с шаблоном {task_template.name} уже существует для взаимодействия {instance.interaction}. Пропускаем создание.")
        return

    logger.debug(f"Задача будет назначена")

    kwargs = {
        'task_template': task_template,
        'assignment': instance,
        'name': task_template.name,
        'task_type': task_template.task_type,
        'is_child': task_template.is_child,
        'item': task_template.item,
        'require_review': task_template.require_review,
        'material': task_template.material,
        'new': task_template.new,
        'course': task_template.course,
        'test': task_template.test,
        'slot_select': task_template.slot_select,
        'event_template': task_template.event_template,
        'event_slot': task_template.event_slot,
        'manual': task_template.manual,
        'desc': task_template.desc,
        'task_outcome': task_template.waiting,
        'waiting': task_template.waiting,
        'interaction': instance.interaction,
    }

    if plan:
        kwargs['plan'] = plan

    if instance.executor_type != 'none':
        kwargs['executor'] = executor

    if task_template.is_child and task_template.delay_type != 'none':
        logger.debug(f"Время начала с задержкой")
        if task_template.delay_type == 'minutes':
            planned_start = instance.planned_start + timedelta(minutes=task_template.delay_value)
            logger.debug(f"Время начала: {planned_start}")
            kwargs['planned_start'] = planned_start
        elif task_template.delay_type == 'hours':
            planned_start = instance.planned_start + timedelta(hours=task_template.delay_value)
            logger.debug(f"Время начала: {planned_start}")
            kwargs['planned_start'] = planned_start
        elif task_template.delay_type == 'days':
            planned_start = instance.planned_start + timedelta(days=task_template.delay_value)
            logger.debug(f"Время начала: {planned_start}")
            kwargs['planned_start'] = planned_start
    else:
        logger.debug(f"Время начала без задержки")
        planned_start = instance.planned_start
        kwargs['planned_start'] = planned_start
        logger.debug(f"Время начала: {planned_start}")

    if task_template.term_type != 'none':

        kwargs['deadline'] = True

        if task_template.term_type == 'minutes':
            kwargs['planned_end'] = planned_start + timedelta(minutes=task_template.term_value)
        elif task_template.term_type == 'hours':
            kwargs['planned_end'] = planned_start + timedelta(hours=task_template.term_value)
        elif task_template.term_type == 'days':
            kwargs['planned_end'] = planned_start + timedelta(days=task_template.term_value)

    logger.debug(f"Данные создаваемой задачи: {kwargs}")

    task, task_created = Task.objects.get_or_create(**kwargs)

    if task_created:

        logger.debug(f"Задача создана: {task.__dict__}")

        if instance.controller_group:
            task.controllers.set(instance.controller_group.user_set.all())
        if instance.observer_group:
            task.observers.set(instance.observer_group.user_set.all())

        task.co_executor_group = AccountsGroup.objects.create(
            name=f"Соисполнители задачи [{task.id}]",
            type='task_co_executors'
        )
        task.controller_group = AccountsGroup.objects.create(
            name=f"Контролеры задачи [{task.id}]",
            type='task_co_controllers'
        )
        task.observer_group = AccountsGroup.objects.create(
            name=f"Наблюдатели задачи [{task.id}]",
            type='task_co_observers'
        )

        task.co_executor_group.user_set.set(task.co_executors.all())
        task.controller_group.user_set.set(task.controllers.all())
        task.observer_group.user_set.set(task.observers.all())

        task.save()

        logger.debug(f"Группы задачи созданы: {task.__dict__}")

        if task.executor:
            assign_perm('view_task', task.executor, task)
            logger.info(f"Права на задачу {task.id} назначены исполнителю {task.executor}")
        assign_perm('view_task', task.co_executor_group, task)
        logger.info(f"Права на задачу {task.id} назначены группе соисполнителей {task.co_executor_group}")

        assign_perm('view_task', task.controller_group, task)
        assign_perm('change_task', task.controller_group, task)
        logger.info(f"Права на задачу {task.id} назначены группе контролёров {task.controller_group}")

        assign_perm('view_task', task.observer_group, task)
        logger.info(f"Права на задачу {task.id} назначены группе наблюдателей {task.observer_group}")

        if task_template.task_type == 'plan_implementation':

            for task_template in task_template.child_tasks.all():
                assignment_task_create(instance=instance, executor=instance.executor, task_template=task_template, plan=task)

def process_events(events, interaction):
    for event in events:
        control_element = event.control_element

        activated = ControlElementActivation.objects.filter(
            control_element=control_element,
            interaction=interaction
        ).exists()

        if not control_element.repeat and activated:
            logger.debug("Управляющий элемент уже срабатывал (repeat=False) — пропуск")
            continue

        if check_control_element_conditions(control_element, interaction):
            logger.debug(f"Все условия выполнены, запускаем действия для {control_element} и взаимодействия {interaction}")
            ControlElementActivation.objects.create(
                control_element=control_element,
                interaction=interaction
            )
        else:
            logger.debug(f"Условия для {control_element} не выполнены для взаимодействия {interaction}")

def check_control_element_conditions(control_element, interaction):
    conditions = control_element.conditions.all()
    chunks = {}  # key=номер куска, value=список условий (AND внутри)
    chunk_index = 0
    current_chunk = []

    for condition in conditions:
        current_chunk.append(condition)
        operator = condition.logic_operator or 'and'
        if operator == 'or':
            chunks[chunk_index] = current_chunk
            chunk_index += 1
            current_chunk = []

    if current_chunk:
        chunks[chunk_index] = current_chunk

    logger.debug(f"Сформированные куски условий для {control_element}: {chunks}")

    # Проверяем каждый кусок через AND
    chunk_results = []
    for chunk_conditions in chunks.values():
        results = []
        for condition in chunk_conditions:
            if condition.condition_type == 'task_exists':
                result = check_task_exists_condition(condition, interaction)
            elif condition.condition_type == 'task_status':
                result = check_task_status_condition(condition, interaction)
            elif condition.condition_type == 'task_outcome':
                result = check_task_outcome_condition(condition, interaction)
            elif condition.condition_type == 'child_tasks_status':
                result = check_child_tasks_status_condition(condition, interaction)
            elif condition.condition_type == 'days_worked':
                result = check_days_worked_condition(condition, interaction)
            else:
                logger.warning(f"Неизвестный тип условия: {condition.condition_type}")
                result = False
            logger.debug(f"Условие {condition} — результат проверки: {result}")
            results.append(result)

        chunk_results.append(all(results))

    final_result = any(chunk_results)
    logger.debug(f"Все условия для {control_element} {'выполнены' if final_result else 'не выполнены'}")
    return final_result

def get_target_task(target_task, task_template, interaction):

    if target_task == 'current':
        return Task.objects.filter(
            interaction=interaction,
            task_template=task_template
        ).order_by('-created').first()

    elif target_task == 'all':
        if interaction.object_type == 'client' and interaction.client:
            return Task.objects.filter(
                task_template=task_template,
                interaction__client=interaction.client
            ).order_by('-created').first()

        elif interaction.object_type == 'account' and interaction.account:
            return Task.objects.filter(
                task_template=task_template,
                interaction__account=interaction.account
            ).order_by('-created').first()

    return None

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

def check_task_exists_condition(condition, interaction):
    task = get_target_task(
        condition.target_task,
        condition.task_template,
        interaction
    )
    task_exists = task is not None
    logger.debug(
        f"Проверка наличия задачи: по условию={condition.boolean_operator}, по факту {task_exists}"
    )
    return task_exists == condition.boolean_operator

def check_task_status_condition(condition, interaction):
    task = get_target_task(condition.target_task, condition.task_template, interaction)

    if not task:
        logger.debug("Нет задачи для условия task_status")
        return False

    result = get_task_result(task)
    if not result:
        logger.debug("Нет результата для задачи")
        return False

    current_status = result.status
    target_status = condition.task_status
    op = condition.comparison_operator

    logger.debug(f"Проверка статуса: текущий={current_status}, целевой={target_status}, оператор={op}")

    if op == 'equal':
        return current_status == target_status
    elif op == 'not_equal':
        return current_status != target_status
    
    logger.warning(f"Неизвестный order_operator: {op}")
    return False

def check_task_outcome_condition(condition, interaction):
    task = get_target_task(condition.target_task, condition.task_template, interaction)

    if not task:
        logger.debug("Нет задачи для условия task_outcome")
        return False

    result = get_task_result(task)
    if not result:
        logger.debug("Нет результата для задачи")
        return False

    current_outcome = result.outcome
    target_outcome = condition.task_outcome
    op = condition.comparison_operator

    logger.debug(f"Проверка итога: текущий={current_outcome}, целевой={target_outcome}, оператор={op}")

    if op == 'equal':
        return current_outcome == target_outcome
    elif op == 'not_equal':
        return current_outcome != target_outcome

    logger.warning(f"Неизвестный order_operator: {op}")
    return False

def check_child_tasks_status_condition(condition, interaction):
    task = get_target_task(condition.target_task, condition.task_template, interaction)

    if not task:
        logger.debug("Нет родительской задачи для child_tasks_status")
        return False

    child_tasks = task.child_tasks.all()

    if not child_tasks.exists():
        logger.debug("Нет дочерних задач")
        return False

    target_status = condition.task_status
    op = condition.comparison_operator

    statuses = []
    for child in child_tasks:
        result = get_task_result(child)
        if result:
            statuses.append(result.status)

    if not statuses:
        logger.debug("Нет статусов у дочерних задач")
        return False

    logger.debug(f"Статусы дочерних задач: {statuses}")

    if op == 'equal':
        return all(s == target_status for s in statuses)
    elif op == 'not_equal':
        return all(s != target_status for s in statuses)

    logger.warning(f"Неизвестный order_operator: {op}")
    return False

def check_days_worked_condition(condition, interaction):
    account = interaction.account or interaction.client.account
    if not account:
        logger.debug("Нет account у interaction для условия days_worked")
        return False

    if not condition.days_worked:
        logger.debug("Не указано значение days_worked в условии")
        return False

    placement = Placement.objects.filter(
        account=account,
        start_date__isnull=False
    ).order_by('-start_date').first()

    if not placement:
        logger.debug(f"У аккаунта {account} нет назначения (Placement)")
        return False

    start_date = placement.start_date
    end_date = placement.end_date

    if not start_date:
        logger.debug("У Placement отсутствует start_date")
        return False


    end_point = end_date or timezone.now().date()
    worked_days = (end_point - start_date).days

    target_days = condition.days_worked
    op = condition.order_operator

    logger.debug(
        f"Проверка стажа: дней стажа={worked_days}, целевое={target_days}, оператор={op}"
    )

    if op == 'gte':
        return worked_days >= target_days
    elif op == 'lte':
        return worked_days <= target_days

    logger.warning(f"Неизвестный order_operator: {op}")
    return False


def execute_control_element_actions(control_element, interaction):
    actions = control_element.actions.all().order_by('item')
    logger.debug(f"Выполняем действия для {control_element}: {list(actions)}")

    for action in actions:
        try:
            if action.action_type == 'change_task_status':
                execute_change_task_status(action, interaction)

            elif action.action_type == 'change_task_outcome':
                execute_change_task_outcome(action, interaction)

            elif action.action_type == 'assign_task':
                execute_assign_task(action, interaction)

            elif action.action_type == 'add_task_to_queue':
                execute_add_task_to_queue(action, interaction)

            elif action.action_type == 'new_interaction':
                execute_new_interaction(action, interaction)

            elif action.action_type == 'add_to_group':
                execute_add_to_group(action, interaction)

            elif action.action_type == 'remove_from_group':
                execute_remove_from_group(action, interaction)

            else:
                logger.warning(f"Неизвестный тип действия: {action.action_type}")

        except Exception as e:
            logger.error(
                f"Ошибка при выполнении действия {action}: {e}",
                exc_info=True
            )


def execute_change_task_status(action, interaction):
    logger.debug(f"Запуск действия {action} для взаимодействия {interaction}")

    if not action.task_template:
        logger.debug(f"Не удалось определить шаблон задачи для действия {action}. Пропускаем создание")
        return

    task = get_target_task(action.target_task, action.task_template, interaction)

    if not task:
        logger.debug(f"Не найдена задача по шаблону {action.task_template}")
        return

    if action.task_status:
        logger.debug(f"Изменяем статус задачи {task} на {action.task_status}")
        result = get_task_result(task)
        if result:
            result.status = action.task_status
            result.save(update_fields=['status', 'changed'])

def execute_change_task_outcome(action, interaction):
    logger.debug(f"Запуск действия {action} для взаимодействия {interaction}")

    if not action.task_template:
        logger.debug(f"Не удалось определить шаблон задачи для действия {action}. Пропускаем создание")
        return

    task = get_target_task(action.target_task, action.task_template, interaction)

    if not task:
        logger.debug(f"Не найдена задача по шаблону {action.task_template}")
        return

    if action.task_outcome:
        logger.debug(f"Изменяем итог задачи {task} на {action.task_outcome}")
        result = get_task_result(task)
        if result:
            result.outcome = action.task_outcome
            result.save(update_fields=['outcome', 'changed'])

def execute_assign_task(action, interaction):
    logger.debug(f"Запуск действия {action} для взаимодействия {interaction}")

    if not action.task_template:
        logger.debug(f"Не удалось определить шаблон задачи для действия {action}. Пропускаем создание")
        return

    if action.target_interaction == 'current':
        target_interaction = interaction

    elif action.target_interaction == 'last':
        if interaction.object_type == 'client' and interaction.client:
            target_interaction = Interaction.objects.filter(client=interaction.client).order_by('-created').first()
        elif interaction.object_type == 'account' and interaction.account:
            target_interaction = Interaction.objects.filter(account=interaction.account).order_by('-created').first()

    if not target_interaction:
        logger.debug(f"Не удалось определить тип взаимодействия для действия {action}. Пропускаем создание.")
        return

    existing_task = Task.objects.filter(
        interaction=target_interaction,
        task_template=action.task_template
    ).first()

    if existing_task:
        logger.debug(f"Задача с шаблоном {action.task_template} уже существует для взаимодействия {target_interaction}. Пропускаем создание.")
        return

    executor = None
    executor_type = 'none'

    if action.executor_type == 'selected_executor':
        executor_type = 'selected'
        executor = action.executor
    elif action.executor_type == 'current_executor':
        last_task = Task.objects.filter(interaction=interaction).order_by('-created').first()
        if last_task and last_task.executor:
            executor_type = 'selected'
            executor = last_task.executor
        else:
            if interaction.object_type == 'account':
                executor = interaction.account

    elif action.executor_type == 'none':
        executor_type = 'none'
        executor = None

    if (action.executor_type == 'selected_executor' or action.executor_type == 'current_executor') and not executor:
        logger.debug(f"Не удалось определить target_interaction для типа {action.interaction_type}. Пропуск.")
        return

    logger.debug(
        f"Создаём назначение шаблона задачи {action.task_template} для взаимодействия {target_interaction}, исполнитель: {executor}"
    )

    assignment_fields = {
        'name': f"{action.task_template.name}",
        'task_template': action.task_template,
        'interaction_type': 'selected',
        'interaction': target_interaction,
        'executor_type': executor_type,
        'executor': executor,
        'manager_control': action.manager_control,
        'controller_group': action.controller_group,
        'observer_group': action.observer_group,
        'planned_start': timezone.now(),
    }
    logger.debug(f"Поля для создания назначения подготовлены: {assignment_fields}")

    assignment = TaskTemplateAssignment.objects.create(**assignment_fields)
    logger.debug(f"Назначение создано: {assignment}")


def execute_add_task_to_queue(action, interaction):
    logger.debug(f"Запуск действия: {action} для взаимодействия {interaction}")

    if not action.task_template:
        logger.debug(f"Не удалось определить шаблон задачи для действия {action}. Пропускаем создание")
        return

    if not action.queue:
        logger.debug(f"Не удалось определить очередь для действия {action}. Пропускаем создание")
        return

    logger.debug(f"Добавляем задачу {action.task_template} для {interaction} в очередь {action.queue}")

    task = get_target_task(action.target_task, action.task_template, interaction)
    if not task:
        logger.debug(f"Не найдена задача по шаблону {action.task_template}")
        return
    if task.executor:
        logger.debug(f"У задачи уже есть исполнитель {task.executor}")
        return
    if QueueTask.objects.filter(task=task, queue=action.queue).exists():
        logger.debug(f"Задача {task} уже присутствует в очереди {action.queue}. ")
        return


    queue_task = QueueTask.objects.create(
        queue=action.queue,
        task=task,
        status='waiting_for_executor',
        item=action.queue.queue_tasks.count() + 1
    )
    logger.debug(f"Задача добавлена в очередь: {queue_task}")

def execute_new_interaction(action, interaction):
    logger.debug(f"Запуск действия: {action} для взаимодействия {interaction}")

    new_interaction = Interaction.objects.create(
        object_type=interaction.object_type,
        client=interaction.client,
        account=interaction.account,
        creator=interaction.creator,
    )

    logger.debug(f"Создано новое взаимодействие {new_interaction}")


def execute_add_to_group(action, interaction):
    logger.debug(f"Запуск действия: {action} для взаимодействия {interaction}")

    if not action.target_group:
        logger.debug(f"Не указана целевая группа для действия {action}. Пропускаем")
        return


    account = interaction.account or interaction.client.account
    if not account:
        logger.debug(f"Не удалось определить account для interaction {interaction}. Пропускаем")
        return

    if action.target_group.user_set.filter(id=account.id).exists():
        logger.debug(
            f"Аккаунт {account} уже состоит в группе {action.target_group}. Пропускаем"
        )
        return

    action.target_group.user_set.add(account)

    logger.debug(
        f"Аккаунт {account} добавлен в группу {action.target_group}"
    )

def execute_remove_from_group(action, interaction):
    logger.debug(f"Запуск действия: {action} для взаимодействия {interaction}")

    if not action.target_group:
        logger.debug(f"Не указана целевая группа для действия {action}. Пропускаем")
        return

    account = interaction.account or interaction.client.account
    if not account:
        logger.debug(f"Не удалось определить account для interaction {interaction}. Пропускаем")
        return

    if not action.target_group.user_set.filter(id=account.id).exists():
        logger.debug(
            f"Аккаунт {account} не состоит в группе {action.target_group}. Пропускаем"
        )
        return

    action.target_group.user_set.remove(account)

    logger.debug(
        f"Аккаунт {account} удалён из группы {action.target_group}"
    )

def send_notifications(notification_type, context, **kwargs):

    if notification_type == 'task_created':
        task = context.get("task")

        # Собираем всех получателей
        recipients = set()

        # Исполнитель
        executor = context.get("executor")
        if executor:
            recipients.add(executor)

        # Соисполнители
        for acc in context.get("co_executors", []):
            recipients.add(acc)

        # Контролёры
        for acc in context.get("controllers", []):
            recipients.add(acc)

        # Наблюдатели
        for acc in context.get("observers", []):
            recipients.add(acc)

        # Создаём оповещения
        for account in recipients:
            TaskNotification.objects.create(
                task=task,
                account=account,
                notification_type="task_created"
            )

        return

def create_task_notifications(task, executors, controllers, observers, notification_type):

    recipients = set()

    for acc in executors:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.self_tasks_tracking:
            recipients.add(acc)

    for acc in controllers:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.controlled_tasks_tracking:
            recipients.add(acc)

    for acc in observers:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.observed_tasks_tracking:
            recipients.add(acc)

    for acc in recipients:
        notification = TaskNotification.objects.create(
            task=task,
            account=acc,
            notification_type=notification_type
        )
        logger.debug(f"Создано оповещение: {notification}")

def check_send_conditions(account, task, role):
    now = timezone.now()
    settings = getattr(account, 'notification_settings', None)
    if role == 'executor':
        reminder_days = (
            settings.self_tasks_reminder_period if settings
            else 1
        )
    elif role == 'controller':
        reminder_days = (
            settings.controlled_tasks_reminder_period if settings
            else 3
        )
    elif role == 'observer':
        reminder_days = (
            settings.observed_tasks_reminder_period if settings
            else 7
        )
    else:
        logger.debug(f"Роль не определена")
        return False
    logger.debug(f"Период оповещений по задаче {task} для пользователя {account} равен {reminder_days}")

    last_notification = TaskNotification.objects.filter(
        task=task,
        notification_type='task_reminder'
    ).order_by('-created').first()

    if last_notification:
        logger.debug(f"Последнее оповещение по задаче создано {last_notification.created}")
        last_activity = last_notification.created
    else:
        logger.debug(f"Оповещение по задаче созданной {task.created} не было")
        last_activity = task.created

    if now < last_activity + timedelta(days=reminder_days):
        logger.debug(f"Оповещения не будет")
        return False
    logger.debug(f"Пользователь будет оповещен")
    return True

def create_task_reminders(task, executors, controllers, observers, notification_type):

    recipients = set()

    for acc in executors:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.self_tasks_tracking:
            need_send = check_send_conditions(acc, task, role='executor')
            if need_send:
                recipients.add(acc)

    for acc in controllers:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.controlled_tasks_tracking:
            need_send = check_send_conditions(acc, task, role='controller')
            if need_send:
                recipients.add(acc)

    for acc in observers:
        settings = getattr(acc, "notification_settings", None)
        if not settings or settings.observed_tasks_tracking:
            need_send = check_send_conditions(acc, task, role='observer')
            if need_send:
                recipients.add(acc)

    for acc in recipients:
        notification = TaskNotification.objects.create(
            task=task,
            account=acc,
            notification_type=notification_type
        )
        logger.debug(f"Создано оповещение: {notification}")

def process_task_notifications(notification_type, context, **kwargs):

    task = context.get("task")

    executors = set()
    controllers = set()
    observers = set()

    executor = context.get("executor")
    if executor:
        executors.add(executor)
    executors.update(context.get("co_executors", []))
    controllers.update(context.get("controllers", []))
    observers.update(context.get("observers", []))

    if notification_type in ['task_created', 'task_completed', 'task_failed', 'task_canceled']:

        create_task_notifications(
            task,
            executors,
            controllers,
            observers,
            notification_type
        )
        logger.debug(f"Создание оповещений по задаче {task} для исполниетлей {executors}, контролеров {controllers} и наблюдателей {observers}")

    if notification_type == 'task_reminder':

        create_task_reminders(
            task,
            executors,
            controllers,
            observers,
            notification_type
        )
        logger.debug(
            f"Создание оповещений по задаче {task} для исполниетлей {executors}, контролеров {controllers} и наблюдателей {observers}")






