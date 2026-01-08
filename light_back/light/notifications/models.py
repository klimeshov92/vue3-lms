from django.db import models
from core.models import Account
from bpms.models import *

# Create your models here.

class NotificationSettings(models.Model):
    account = models.OneToOneField(
        Account,
        verbose_name='Аккаунт',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notification_settings',
        related_query_name='notification_settings'
    )
    self_tasks_tracking = models.BooleanField('Отслеживание своих задач', default=True)
    controlled_tasks_tracking = models.BooleanField('Отслеживание задач на контроле', default=True)
    observed_tasks_tracking = models.BooleanField('Отслеживание задач под наблюдением', default=True)
    self_tasks_reminder_period = models.PositiveIntegerField('Период напоминания для своих задач (дней)', default=1)
    controlled_tasks_reminder_period = models.PositiveIntegerField('Период напоминания для задач на контроле (дней)', default=3)
    observed_tasks_reminder_period = models.PositiveIntegerField('Период напоминания для задач под наблюдением (дней)', default=7)

    class Meta:
        verbose_name = 'Настройки уведомлений'
        verbose_name_plural = 'Настройки уведомлений'
        default_permissions = ()
        permissions = (
            ('add_notification_settings', 'Может добавлять настройки уведомлений'),
            ('change_notification_settings', 'Может изменить настройки уведомлений'),
            ('delete_notification_settings', 'Может удалить настройки уведомлений'),
            ('view_notification_settings', 'Может просматривать настройки уведомлений'),
        )

    def __str__(self):
        return self.account.username

class TaskNotification(models.Model):
    task = models.ForeignKey(
        Task,
        related_name='notifications',
        related_query_name='notification',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    account = models.ForeignKey(
        Account,
        verbose_name='Аккаунт',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_notifications',
        related_query_name='task_notification'
    )
    NOTIFICATION_TYPES = [
        ('task_created', 'Создание задачи'),
        ('task_reminder', 'Напоминание о задаче'),
        ('task_completed', 'Выполнение задачи'),
        ('task_failed', 'Провал задачи'),
        ('task_canceled', 'Отмена задачи'),
    ]
    notification_type = models.CharField('Тип оповещения', max_length=50, choices=NOTIFICATION_TYPES, null=True, blank=True)
    read = models.BooleanField('Прочитано', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)

    class Meta:
        verbose_name = 'Оповещение о задаче'
        verbose_name_plural = 'Оповещения о задаче'
        default_permissions = ()
        permissions = (
            ('add_task_notification', 'Может добавить оповещение о задаче'),
            ('change_task_notification', 'Может изменить оповещение о задаче'),
            ('delete_task_notification', 'Может удалить оповещение о задаче'),
            ('view_task_notification', 'Может просматривать оповещение о задаче'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_notification_type_display()} - {self.created.strftime("%d.%m.%Y %H:%M")}'