from django.db import models
from core.models import *
from materials.models import *
from files.models import *

# Create your models here.

class EventTemplate(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='event_template_avatars/')
    FORMATS = [
        ('face_to_face', 'Очное мероприятие'),
        ('webinar', 'Вебинар'),
        ('mixed', 'Смешанный формат'),
    ]
    format = models.CharField(max_length=255, choices=FORMATS, null=True, blank=True, verbose_name='Формат')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='event_templates',
        related_query_name='event_templates',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    link = models.TextField(verbose_name='Ссылка',  null=True, blank=True)
    location = models.TextField(verbose_name='Локация', null=True, blank=True)
    admins = models.ManyToManyField(
        Account,
        verbose_name='Ведущие',
        related_name='event_templates_admins',
        related_query_name='event_templates_admin',
        db_index=True
    )
    admin_group = models.OneToOneField(
        AccountsGroup,
        verbose_name='Группа ведущих',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='event_templates_admins',
        related_query_name='event_templates_admins'
    )
    TERM_TYPES = [
        ('minutes', 'Минуты'),
        ('hours', 'Часы'),
        ('days', 'Дни'),
        ('none', 'Без срока'),
    ]
    #term_type = models.CharField('Тип срока', max_length=20, choices=TERM_TYPES, null=True, blank=True)
    #term_value = models.IntegerField('Срок', null=True, blank=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_template_creators',
        related_query_name='event_template_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_template_editors',
        related_query_name='event_template_editor'
    )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        default_permissions = ()
        permissions = (
            ('add_event_template', 'Может добавить мероприятие'),
            ('change_event_template', 'Может изменить мероприятие'),
            ('delete_event_template', 'Может удалить мероприятие'),
            ('view_event_template', 'Может просматривать мероприятие'),
        )

    def __str__(self):
        return f'{self.name}'

class EventSlot(models.Model):
    event_template = models.ForeignKey(
        EventTemplate,
        related_name='event_slots',
        related_query_name='event_slot',
        verbose_name='Мероприятие',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    number_of_participants = models.PositiveIntegerField('Количество участников', null=True, blank=True)
    registration = models.BooleanField('Регистрация открыта', default=False)
    planned_start = models.DateTimeField('Начало по плану', null=True, blank=True)
    deadline = models.BooleanField('Сроки', default=False)
    planned_end = models.DateTimeField('Конец по плану', null=True, blank=True)
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    STATUSES = [
        ('planned', 'Планируется'),
        ('canceled', 'Отменено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]
    status = models.CharField(max_length=64, choices=STATUSES, default='planned', verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_slot_creators',
        related_query_name='event_slot_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_slot_editors',
        related_query_name='event_slot_editor'
    )

    class Meta:
        verbose_name = 'Слот мероприятия'
        verbose_name_plural = 'Слот мероприятия'
        default_permissions = ()
        permissions = (
            ('add_event_slot', 'Может добавить слот мероприятия'),
            ('change_event_slot', 'Может изменить слот мероприятия'),
            ('delete_event_slot', 'Может удалить слот мероприятия'),
            ('view_event_slot', 'Может просматривать слот мероприятия'),
        )

    def __str__(self):
        return f'{self.event_template.name} - {self.planned_start.strftime("%d.%m.%Y %H:%M")}'
