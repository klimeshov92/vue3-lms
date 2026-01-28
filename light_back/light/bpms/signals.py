
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponseServerError
from .models import *
from comments.models import *
from datetime import datetime, timedelta
from django.db import transaction
from .functions import *
from django.contrib.contenttypes.models import ContentType
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger('project')

@receiver(post_save, sender=Task)
def task_result_create(sender, instance, created, **kwargs):
    try:

        logger.debug(f"Начало работы сигнала task_result_create")

        if created:

            logger.debug(f"Создание результата для задачи: {instance.__dict__}")

            if instance.task_type == 'common_task':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = TaskResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'plan_implementation':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = PlanResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'news_reading':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = NewResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'material_review':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = MaterialResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'course_study':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = CourseResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'test_taking':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = TestResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

            if instance.task_type == 'event_participation':

                kwargs = {
                    'task': instance,
                    'creator': instance.creator,
                }

                if instance.waiting:
                    kwargs['status'] = 'waiting'
                else:
                    kwargs['status'] = 'assigned'

                result, result_created = EventResult.objects.get_or_create(**kwargs)

                if result_created:
                    logger.debug(f"Результат создан: {result.__dict__}")

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала task_result_create: {e}", exc_info=True)
        if settings.DEBUG:
            raise

@receiver(post_save, sender=Task)
def task_comments_create(sender, instance, created, **kwargs):
    try:

        logger.debug(f"Начало работы сигнала task_comments_create")
        if created:

            topic, topic_created = Topic.objects.get_or_create(
                topic_type='task_topic',
                task=instance,
                name=f'Топик задачи {instance.name}',
            )
            if topic_created:
                logger.debug(f"Топик создан: {topic.__dict__}")

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала task_comments_create: {e}", exc_info=True)
        if settings.DEBUG:
            raise

@receiver(post_delete, sender=Task)
def task_group_delete(sender, instance, **kwargs):
    try:

        logger.debug(f"Начало работы сигнала task_group_delete")

        if instance.co_executor_group:
            instance.co_executor_group.delete()
        if instance.controller_group:
            instance.controller_group.delete()
        if instance.observer_group:
            instance.observer_group.delete()

        logger.debug(f"Связанные с задачей группы удалены")

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала task_group_delete: {e}", exc_info=True)
        if settings.DEBUG:
            raise

@receiver(post_save, sender=TaskTemplateAssignment)
def task_template_assignment_task_create(sender, instance, created, **kwargs):
    try:
        logger.debug(f"Начало работы сигнала task_template_assignment_task_create")

        if created:
            if instance.executor_type == 'selected' or instance.executor_type == 'none':

                logger.debug(f"Назначение задачи выбранному исполнителю: {instance.executor}")

                assignment_task_create(instance=instance, executor=instance.executor, task_template=instance.task_template)

            elif instance.executor_type == 'group':

                executors = instance.executor_group.user_set.all()

                logger.debug(f"Назначение задачи группе: {executors}")

                for executor in executors:

                    assignment_task_create(instance=instance, executor=executor, task_template=instance.task_template)

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала task_template_assignment_task_create: {e}", exc_info=True)
        if settings.DEBUG:
            raise

@receiver(pre_save, sender=TaskResult)
def task_result_passing_old_condition(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        instance._old_outcome = None
        return

    old = sender.objects.get(pk=instance.pk)
    instance._old_status = old.status
    instance._old_outcome = old.outcome

@receiver(post_save, sender=TaskResult)
def send_task_notifications(sender, instance, created, **kwargs):
    try:
        send = False

        if created:
            notification_type = 'task_created'
            send = True

        if not created and instance._old_status != instance.status:
            if instance.status == 'completed':
                notification_type = 'task_completed'
                send = True
            if instance.status == 'failed':
                notification_type = 'task_failed'
                send = True
            if instance.status == 'canceled':
                notification_type = 'task_canceled'
                send = True

        if send:
            task = instance.task

            context = {
                "task": task,
                "executor": task.executor,
                "co_executors": task.co_executors.all(),
                "controllers": task.controllers.all(),
                "observers": task.observers.all(),
            }

            process_task_notifications(notification_type=notification_type, context=context)

    except Exception as e:
        logger.error(
            f"Ошибка в send_task_notifications: {e}",
            exc_info=True
        )
        if settings.DEBUG:
            raise

@receiver(post_save, sender=TaskResult)
def task_result_events(sender, instance, created, **kwargs):
    try:
        if created:
            logger.debug("TaskResult создан впервые — пропускаем обработку изменений.")
            return

        task = instance.task
        if not task.task_template or not task.interaction:
            return

        if instance._old_status != instance.status:
            logger.debug(
                f"Статус задачи изменён: {instance._old_status} → {instance.status}"
            )

            events = ControlElementEvent.objects.filter(
                event_type='task_status_changed',
                task_template=task.task_template
            ).select_related('control_element')

            process_events(events, task.interaction)

            # Дочерние задачи
            if task.is_child and task.plan:
                parent_events = ControlElementEvent.objects.filter(
                    event_type='child_task_status_changed',
                    task_template=task.plan.task_template
                ).select_related('control_element')

                process_events(parent_events, task.plan.interaction)

        if instance._old_outcome != instance.outcome:
            logger.debug(
                f"Итог задачи изменён: {instance._old_outcome} → {instance.outcome}"
            )

            events = ControlElementEvent.objects.filter(
                event_type='task_outcome_changed',
                task_template=task.task_template
            ).select_related('control_element')

            process_events(events, task.interaction)

    except Exception as e:
        logger.error(
            f"Ошибка в task_result_post_save: {e}",
            exc_info=True
        )
        if settings.DEBUG:
            raise

@receiver(post_save, sender=ControlElementActivation)
def execute_actions_on_activation(sender, instance, created, **kwargs):
    if not created:
        return

    control_element = instance.control_element
    interaction = instance.interaction

    logger.debug(
        f"Запуск действий по срабатыванию {instance} "
        f"для элемента {control_element} и взаимодействия {interaction}"
    )

    try:
        execute_control_element_actions(control_element, interaction)

        events = ControlElementEvent.objects.filter(
            event_type='trigger_fired',
            fired_trigger=control_element
        ).exclude(
            control_element=control_element
        ).select_related('control_element')
        if events.exists():
            process_events(events, interaction)

    except Exception as e:
        logger.error(
            f"Ошибка при выполнении действий для {control_element} и взаимодействия {interaction}: {e}",
            exc_info=True
        )
        if settings.DEBUG:
            raise

@receiver(post_save, sender=QueueTask)
def queue_task_executor_choice(sender, instance, created, **kwargs):
    try:
        logger.debug("Начало работы queue_task_executor_choice")

        if not created:
            return

        queue = instance.queue
        task = instance.task

        if not queue.auto_assignment:
            logger.debug("Автоназначение отключено — пропуск")
            return

        # Получаем исполнителей, отсортированных по item
        executors = list(queue.queue_executors.order_by("item"))

        if not executors:
            logger.debug(f"В очереди {queue} нет исполнителей — пропуск")
            return

        # Корректируем индекс, если вышел за границы
        idx = queue.last_executor_idx
        if idx >= len(executors):
            idx = 0

        # Забираем исполнителя.
        queue_executor = executors[idx]
        executor = queue_executor.executor

        logger.debug(f"Назначаем исполнителя {executor}")

        def assign_executor(task, executor):

            task.executor = executor
            task.save(update_fields=["executor", "changed"])

            logger.debug(f"В задачу {task} назначен исполнитель {executor}")

            if task.executor:
                assign_perm('view_task', task.executor, task)
                logger.info(
                    f"Права на задачу {task.id} назначены исполнителю {task.executor}"
                )

                if task.task_type == 'material_review' and task.material:
                    assign_perm('view_material', task.executor, task.material)
                    logger.info(
                        f"Права на материал {task.material.id} назначены исполнителю {task.executor}"
                    )

                    material_topic = task.material.topics.first()
                    if material_topic:
                        assign_perm('view_topic', task.executor, material_topic)
                        logger.info(
                            f"Права на топик материала {material_topic.id} назначены исполнителю {task.executor}"
                        )

                elif task.task_type == 'news_reading' and task.new:
                    assign_perm('view_new', task.executor, task.new)
                    logger.info(
                        f"Права на новость {task.new.id} назначены исполнителю {task.executor}"
                    )

                    new_topic = task.new.topics.first()
                    if new_topic:
                        assign_perm('view_topic', task.executor, new_topic)
                        logger.info(
                            f"Права на топик новости {new_topic.id} назначены исполнителю {task.executor}"
                        )

                elif task.task_type == 'test_taking' and task.test:
                    assign_perm('view_test', task.executor, task.test)
                    logger.info(
                        f"Права на тест {task.test.id} назначены исполнителю {task.executor}"
                    )

                    test_topic = task.test.topics.first()
                    if test_topic:
                        assign_perm('view_topic', task.executor, test_topic)
                        logger.info(
                            f"Права на топик теста {test_topic.id} назначены исполнителю {task.executor}"
                        )

                elif task.task_type == 'course_study' and task.course:
                    assign_perm('view_course', task.executor, task.course)
                    logger.info(
                        f"Права на курс {task.course.id} назначены исполнителю {task.executor}"
                    )

                    course_topic = task.course.topics.first()
                    if course_topic:
                        assign_perm('view_topic', task.executor, course_topic)
                        logger.info(
                            f"Права на топик курса {course_topic.id} назначены исполнителю {task.executor}"
                        )

                elif task.task_type == 'event_participation' and task.event_template:
                    assign_perm('view_event_template', task.executor, task.event_template)
                    logger.info(
                        f"Права на мероприятие {task.event_template.id} назначены исполнителю {task.executor}"
                    )

                    event_topic = task.event_template.topics.first()
                    if event_topic:
                        assign_perm('view_topic', task.executor, event_topic)
                        logger.info(
                            f"Права на топик мероприятия {event_topic.id} назначены исполнителю {task.executor}"
                        )

        assign_executor(task=task, executor=executor)

        if task.task_type == 'plan':
            for child_task in task.child_tasks.all():
                assign_executor(task=child_task, executor=executor)

        # Переход к следующему индексу
        queue.last_executor_idx = idx + 1
        queue.save(update_fields=["last_executor_idx"])

        # Назначаем в QueueTask, если он изменился
        instance.executor = executor
        instance.save(update_fields=["executor"])

    except Exception as e:
        logger.error(f"Ошибка в queue_task_executor_choice: {e}", exc_info=True)
        if settings.DEBUG:
            raise

@receiver(post_save, sender=ControlElementEvent)
def work_time_create(sender, instance, created, **kwargs):
    try:
        logger.debug("Начало работы сигнала work_time_create")

        if not created:
            return

        if not instance.start_time:
            logger.warning(f"У действия {instance.id} нет start_time — work_time не назначено.")
            return

        if instance.period == "daily":
            instance.work_time = instance.start_time + timedelta(days=1)

        elif instance.period == "weekly":
            instance.work_time = instance.start_time + timedelta(weeks=1)

        elif instance.period == "monthly":
            instance.work_time = instance.start_time + relativedelta(months=1)

        else:
            logger.warning(f"Неизвестный период у действия {instance.id}")
            return

        instance.save(update_fields=["work_time"])
        logger.info(f"Начальное work_time для действия {instance.id} = {instance.work_time}")

    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала work_time_create: {e}", exc_info=True)
        if settings.DEBUG:
            raise
