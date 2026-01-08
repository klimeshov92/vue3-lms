from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from guardian.shortcuts import assign_perm
from bpms.models import Task, TaskResult, ControlElementEvent, Interaction
from bpms.functions import *

from bpms.functions import process_events


import logging
logger = logging.getLogger("project")


# Получение результата задачи.
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


# Просто проставить failed всем просроченным задачам.
def process_task_deadlines():
    now = timezone.now()

    # Берём задачи, у которых включён дедлайн и время истекло.
    expired_tasks = Task.objects.filter(
        deadline=True,
        planned_end__lt=now,
    ).select_related("task_template")

    logger.info(f"[DEADLINE] Найдено просроченных задач: {expired_tasks.count()}")

    for task in expired_tasks:

        # Берём результат задачи
        result = get_task_result(task)
        if not result:
            logger.warning(f"[DEADLINE] У задачи {task.id} нет результата. Пропускаем.")
            continue

        # Уже завершённые не трогаем
        if result.status in ["completed", "failed", "canceled"]:
            continue

        logger.info(f"[DEADLINE] Просрочка. Задача {task.id} → FAILED")

        # Ставим провалено
        result.status = "failed"
        result.end_time = now
        result.save(update_fields=["status", "end_time", "changed"])

# События.
def process_periodic_events():
    now = timezone.now()

    logger.info(
        f"[PERIODIC] Запуск проверки переодических событий"
    )

    periodic_events = ControlElementEvent.objects.filter(
        event_type="periodic_event"
    ).select_related("control_element")
    logger.warning(f"[PERIODIC] Периодические события {periodic_events}.")

    for event in periodic_events:

        # Если начало цикла не настало - пропускаем.
        if event.start_time and now < event.start_time:
            logger.warning(f"[PERIODIC] Начало периода срабатывания {event.start_time} не наступило.")
            continue

        # Если work_time отсутствует — некорректная настройка.
        if not event.work_time:
            logger.warning(f"[PERIODIC] У события {event.id} нет work_time. Пропускаем.")
            continue

        # Если время выполнения ещё не наступило — пропускаем.
        if now < event.work_time:
            logger.warning(f"[PERIODIC] Время срабатывания {event.work_time} не наступило.")
            continue

        # Отработка.
        logger.info(f"[PERIODIC] Срабатывание события {event.id} ({event.period})")

        interactions = Interaction.objects.filter(
            task__task_template=event.task_template
        ).distinct()

        logger.info(f"[PERIODIC] Взаимодействия затронутые событием {interactions}")

        for interaction in interactions:
            process_events([event], interaction)

        # Обновляем work_time в зависимости от периодичности
        if event.period == "daily":
            next_fire = event.work_time + timedelta(days=1)

        elif event.period == "weekly":
            next_fire = event.work_time + timedelta(weeks=1)

        elif event.period == "monthly":
            # Правильная обработка месяца
            next_fire = event.work_time + relativedelta(months=1)

        else:
            continue

        # Обновляем время следующего запуска
        event.work_time = next_fire
        event.save(update_fields=["work_time"])

        logger.info(
            f"[PERIODIC] Следующее срабатывание события {event.id} назначено на {next_fire}"
        )

# Напоминания.
def process_task_reminders():
    now = timezone.now()

    logger.info(f"[REMINDER] Проверка напоминаний по задачам")

    tasks = Task.objects.filter(
        deadline=True,
        planned_end__isnull=False
    )
    logger.info(f"[REMINDER] Задачи требующие напоминания {tasks}")

    for task in tasks:
        result = get_task_result(task)
        if not result:
            continue

        # Только активные задачи.
        if result.status not in ['assigned', 'in_progress']:
            continue

        # Уже есть напоминание сегодня — не шлём.
        if TaskNotification.objects.filter(
            task=task,
            notification_type='task_reminder',
            created__date=now.date()
        ).exists():
            continue

        # Отправляем уведомление.
        process_task_notifications(
            notification_type='task_reminder',
            context={
                'task': task,
                'executor': task.executor,
                'co_executors': task.co_executors.all(),
                'controllers': task.controllers.all(),
                'observers': task.observers.all(),
            }
        )

        logger.info(f"[REMINDER] Отправлено напоминание по задаче {task.id}")


class Command(BaseCommand):
    # python manage.py runapscheduler
    help = "Runs APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        # 1. Проверка дедлайнов — КАЖДЫЙ ЧАС
        scheduler.add_job(
            process_task_deadlines,
            trigger=CronTrigger(minute="0"),
            # trigger=CronTrigger(second="*/10"),
            id="task_deadlines",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена ежечасная задача task_deadlines")

        # 2. Периодические события — КАЖДЫЙ ЧАС
        scheduler.add_job(
            process_periodic_events,
            trigger=CronTrigger(minute="0"),
            # trigger=CronTrigger(second="*/10"),
            id="periodic_events",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена ежечасная задача periodic_events")

        # 2. Напоминания о задачах — КАЖДЫЙ ЧАС
        scheduler.add_job(
            process_task_reminders,
            trigger=CronTrigger(hour="9"),
            # trigger=CronTrigger(second="*/10"),
            id="task_reminders",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача напоминаний task_reminders")

        try:
            logger.info("Запуск APScheduler…")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка APScheduler…")
            scheduler.shutdown()
            logger.info("Планировщик остановлен.")
