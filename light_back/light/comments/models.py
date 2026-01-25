from django.db import models

# Create your models here.

from django.db import models
from core.models import *
from bpms.models import *
from news.models import *
from materials.models import *
from courses.models import *
from tests.models import *
from events.models import *




# Create your models here.

class Topic(models.Model):
    TOPICS_TYPES = [
        ('common_topic', 'Обычный топик'),
        ('task_topic', 'Топик задачи'),
        ('queue_topic', 'Топик очереди'),
        ('public_plan_topic', 'Топик плана'),
        ('public_task_topic', 'Топик задания'),
        ('new_topic', 'Топик новости'),
        ('material_topic', 'Топик материала'),
        ('course_topic', 'Топик курса'),
        ('test_topic', 'Топик теста'),
        ('event_template_topic', 'Топик мероприятия'),
        ('event_slot_topic', 'Топик слота мероприятия'),
    ]
    topic_type = models.CharField('Тип топика', max_length=20, choices=TOPICS_TYPES, null=True, blank=True)
    task = models.ForeignKey(
        Task,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    queue = models.ForeignKey(
        Queue,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Очередь',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    public_plan = models.ForeignKey(
        PublicPlan,
        related_name='topics',
        related_query_name='topic',
        verbose_name='План',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    public_task = models.ForeignKey(
        PublicTask,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Задание',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    new = models.ForeignKey(
        New,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Новость',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Материал',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Курс',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    test = models.ForeignKey(
        Test,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Тест',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    event_template = models.ForeignKey(
        EventTemplate,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Шаблон мероприятия',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    event_slot = models.ForeignKey(
        EventSlot,
        related_name='topics',
        related_query_name='topic',
        verbose_name='Слот мероприятия',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='topics',
        related_query_name='topic'
    )
    name = models.CharField(verbose_name='Название', max_length=255, null=True, blank=True, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='topic_creators',
        related_query_name='topic_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='topic_editors',
        related_query_name='topic_editor'
    )

    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'
        default_permissions = ()
        permissions = (
            ('add_topic', 'Может добавить топик'),
            ('change_topic', 'Может изменить топик'),
            ('delete_topic', 'Может удалить топик'),
            ('view_topic', 'Может просматривать топик'),
        )


    def __str__(self):
        return f"{self.get_topic_type_display()} - {self.name}"

class Comment(models.Model):
    topic = models.ForeignKey(
        Topic,
        verbose_name='Топик',
        related_name='messages',
        related_query_name='message',
        on_delete=models.CASCADE
    )
    parent_message = models.ForeignKey(
        'self',
        related_name='child_messages',
        related_query_name='child_message',
        verbose_name='Родительское сообщение',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    sender = models.ForeignKey(
        Account,
        verbose_name='Отправитель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='topic_senders',
        related_query_name='topic_sender'
    )
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name = 'Сообщение топика'
        verbose_name_plural = 'Сообщения топика'
        default_permissions = ()
        permissions = (
            ('add_message', 'Может добавить сообщение'),
            ('change_message', 'Может изменить сообщение'),
            ('delete_message', 'Может удалить сообщение'),
            ('view_message', 'Может просматривать сообщение'),
        )

    def __str__(self):
        return f"{self.topic.name} - {self.id}"

