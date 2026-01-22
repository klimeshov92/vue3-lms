from django.db import models
from core.models import *
from news.models import *
from materials.models import *
from courses.models import *
from tests.models import *
from events.models import *

# Create your models here.

class Interaction(models.Model):
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='interactions',
        related_query_name='interaction'
    )
    OBJECT_TYPES = [
        ('client', 'Клиент'),
        ('account', 'Аккаунт'),
    ]
    object_type = models.CharField('Тип объекта', max_length=50, choices=OBJECT_TYPES, null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Клиент',
        related_name='interactions',
        related_query_name='interaction'
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Аккаунт',
        related_name='interactions',
        related_query_name='interaction'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='interaction_creators',
        related_query_name='interaction_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='editors',
        related_query_name='interaction_editor'
    )

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
        default_permissions = ()
        permissions = (
            ('add_interaction', 'Может добавить взаимодействие'),
            ('change_interaction', 'Может изменить взаимодействие'),
            ('delete_interaction', 'Может удалить взаимодействие'),
            ('view_interaction', 'Может просматривать взаимодействие'),
        )

    def __str__(self):
        if self.object_type == 'client':
            object_name = self.client if self.client else 'Объект не найден'
        elif self.object_type == 'account':
            object_name = self.account if self.account else 'Объект не найден'
        return f'{self.id} - {self.get_object_type_display()} - {object_name}'

class TaskTemplate(models.Model):
    # Тип объекта
    #object_type = models.CharField('Тип объекта', max_length=50, choices=Interaction.OBJECT_TYPES, null=True, blank=True)
    # Для планов
    is_child = models.BooleanField('Дочерняя', default=False)
    plan = models.ForeignKey(
        'self',
        related_name='child_tasks',
        related_query_name='child_task',
        verbose_name='План',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField('Пункт', null=True, blank=True)
    #sub_item = models.PositiveIntegerField('Подпункт', null=True, blank=True)
    DELAY_TYPES = [
        ('minutes', 'Минуты'),
        ('hours', 'Часы'),
        ('days', 'Дни'),
        ('none', 'Без задержки'),
    ]
    delay_type = models.CharField('Тип задержки', max_length=20, choices=DELAY_TYPES, null=True, blank=True)
    delay_value = models.PositiveIntegerField('Задержка', null=True, blank=True)
    # Выбор типа
    TASK_TYPES = [
        ('common_task', 'Обычная задача'),
        ('plan_implementation', 'Реализация плана'),
        ('news_reading', 'Чтение новостей'),
        ('material_review', 'Ознакомление с материалом'),
        ('test_taking', 'Прохождение теста'),
        ('course_study', 'Изучение курса'),
        ('event_participation', 'Участие в мероприятии'),
    ]
    task_type = models.CharField('Тип задачи', max_length=50, choices=TASK_TYPES, null=True, blank=True)
    # Выполнение работы или реализация плана
    manual = models.TextField(verbose_name='Инструкция', blank=True, null=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    # Обычная задача и реализация плана
    require_review = models.BooleanField('Требуется проверка', default=False)
    # Изучение новости
    new = models.ForeignKey(
        New,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Новость',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Изучение материала
    material = models.ForeignKey(
        Material,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Материал',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Прохождение курса
    course = models.ForeignKey(
        Course,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Курс',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Выполнение теста
    test = models.ForeignKey(
        Test,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Тест',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Участие в мероприятии
    event_template = models.ForeignKey(
        EventTemplate,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Мероприятие',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    slot_select = models.BooleanField('Выбор слота', default=True)
    event_slot = models.ForeignKey(
        EventSlot,
        related_name='task_templates',
        related_query_name='task_template',
        verbose_name='Слот мероприятия',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Общие
    task_outcome = models.BooleanField('Итог задачи', default=False)
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='task_templates',
        related_query_name='task_template'
    )
    TERM_TYPES = [
        ('minutes', 'Минуты'),
        ('hours', 'Часы'),
        ('days', 'Дни'),
        ('none', 'Без срока'),
    ]
    term_type = models.CharField('Тип срока', max_length=20, choices=TERM_TYPES, null=True, blank=True)
    term_value = models.IntegerField('Срок', null=True, blank=True)
    waiting = models.BooleanField('Ожидает активации', default=False)
    self_assignment = models.BooleanField('Самоназначение', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_template_creators',
        related_query_name='task_template_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_template_editors',
        related_query_name='task_template_editor'
    )
    class Meta:
        verbose_name = 'Шаблон задачи'
        verbose_name_plural = 'Шаблоны задач'
        default_permissions = ()
        permissions = (
            ('add_task_template', 'Может добавить шаблон задачи'),
            ('change_task_template', 'Может изменить шаблон задачи'),
            ('delete_task_template', 'Может удалить шаблон задачи'),
            ('view_task_template', 'Может просматривать шаблон задачи'),
        )

    def __str__(self):
        if self.item:
            return f'{self.get_task_type_display()} - {self.item} - {self.name}'
        else:
            return f'{self.get_task_type_display()} - {self.name}'

class PublicPlan(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='public_plan_avatars/')
    task_template = models.ForeignKey(
        TaskTemplate,
        verbose_name='Шаблон задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_template_public_plans',
        related_query_name='task_template_public_plan'
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='public_plans',
        related_query_name='public_plan'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='public_plan_creators',
        related_query_name='public_plan_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='public_plan_editors',
        related_query_name='public_plan_editor'
    )

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задание'
        default_permissions = ()
        permissions = (
            ('add_public_plan', 'Может добавить план'),
            ('change_public_plan', 'Может изменить план'),
            ('delete_public_plan', 'Может удалить план'),
            ('view_public_plan', 'Может просматривать план'),
        )
    def __str__(self):
        return f'{self.name}'

class PublicTask(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='public_task_avatars/')
    task_template = models.ForeignKey(
        TaskTemplate,
        verbose_name='Шаблон задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_template_public_tasks',
        related_query_name='task_template_public_task'
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='public_tasks',
        related_query_name='public_task'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='public_task_creators',
        related_query_name='public_task_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='public_task_editors',
        related_query_name='public_task_editor'
    )

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задание'
        default_permissions = ()
        permissions = (
            ('add_public_task', 'Может добавить задание'),
            ('change_public_task', 'Может изменить задание'),
            ('delete_public_task', 'Может удалить задание'),
            ('view_public_task', 'Может просматривать задание'),
        )
    def __str__(self):
        return f'{self.name}'

class Task(models.Model):
    # Шаблон
    task_template = models.ForeignKey(
        TaskTemplate,
        verbose_name='Шаблон задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_template_tasks',
        related_query_name='task_template_task'
    )
    # Назначение
    assignment = models.ForeignKey(
        'TaskTemplateAssignment',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='tasks',
        related_query_name='task'
    )
    # Тип объекта
    #object_type = models.CharField('Тип объекта', max_length=50, choices=Interaction.OBJECT_TYPES, null=True, blank=True)
    interaction = models.ForeignKey(
        Interaction,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Взаимодействие',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    # Для планов
    is_child = models.BooleanField('Дочерняя', default=False)
    plan = models.ForeignKey(
        'self',
        related_name='child_tasks',
        related_query_name='child_task',
        verbose_name='План',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField('Пункт', null=True, blank=True)
    #sub_item = models.PositiveIntegerField('Подпункт', null=True, blank=True)
    # Выбор типа
    TASK_TYPES = [
        ('common_task', 'Обычная задача'),
        ('plan_implementation', 'Реализация плана'),
        ('news_reading', 'Чтение новостей'),
        ('material_review', 'Ознакомление с материалом'),
        ('test_taking', 'Прохождение теста'),
        ('course_study', 'Изучение курса'),
        ('event_participation', 'Участие в мероприятии'),
    ]
    task_type = models.CharField('Тип задачи', max_length=50, choices=TASK_TYPES, null=True, blank=True)
    # Обычная задача и реализация плана
    require_review = models.BooleanField('Требуется проверка', default=False)
    # Изучение новости
    new = models.ForeignKey(
        New,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Новость',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Изучение материала
    material = models.ForeignKey(
        Material,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Материал',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Прохождение курса
    course = models.ForeignKey(
        Course,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Курс',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Выполнение теста
    test = models.ForeignKey(
        Test,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Тест',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Участие в мероприятии
    event_template = models.ForeignKey(
        EventTemplate,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Мероприятие',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    slot_select = models.BooleanField('Выбор слота', default=True)
    event_slot = models.ForeignKey(
        EventSlot,
        related_name='tasks',
        related_query_name='task',
        verbose_name='Слот мероприятия',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Общие
    task_outcome = models.BooleanField('Итог задачи', default=False)
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    manual = models.TextField(verbose_name='Инструкция', blank=True, null=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    planned_start = models.DateTimeField('Начало по плану', null=True, blank=True)
    deadline = models.BooleanField('Сроки', default=False)
    planned_end = models.DateTimeField('Конец по плану', null=True, blank=True)
    waiting = models.BooleanField('Ожидает активации', default=False)
    executor = models.ForeignKey(
        Account,
        related_name='task_executors',
        related_query_name='task_executor',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    co_executors = models.ManyToManyField(
        Account,
        verbose_name='Соисполнители',
        blank=True,
        related_name='task_co_executors',
        related_query_name='task_co_executor',
    )
    co_executor_group = models.OneToOneField(
        AccountsGroup,
        related_name='task_co_executor_group',
        related_query_name='task_co_executor_group',
        verbose_name='Группа соисполнителей',
        null=True,
        blank=True,
        on_delete = models.PROTECT
    )
    controllers = models.ManyToManyField(
        Account,
        verbose_name='Контролеры',
        blank=True,
        related_name='task_controllers',
        related_query_name='task_controller',
    )
    controller_group = models.OneToOneField(
        AccountsGroup,
        related_name='task_controller_group',
        related_query_name='task_controller_group',
        verbose_name='Группа контролеров',
        null=True,
        blank=True,
        on_delete = models.PROTECT
    )
    observers = models.ManyToManyField(
        Account,
        verbose_name='Наблюдатели',
        blank=True,
        related_name='task_observers',
        related_query_name='task_observer',
    )
    observer_group = models.OneToOneField(
        AccountsGroup,
        related_name='task_observer_group',
        related_query_name='task_observer_group',
        verbose_name='Группа наблюдателей',
        null=True,
        blank=True,
        on_delete = models.PROTECT
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='tasks',
        related_query_name='task'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_creators',
        related_query_name='task_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_editors',
        related_query_name='task_editor'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        default_permissions = ()
        permissions = (
            ('add_task', 'Может добавить задачу'),
            ('change_task', 'Может изменить задачу'),
            ('delete_task', 'Может удалить задачу'),
            ('view_task', 'Может просматривать задачу'),
            ('view_analytics', 'Может просматривать аналитику'),
        )
    def __str__(self):
        if self.item:
            return f'{self.get_task_type_display()} - {self.item} - {self.name}'
        else:
            return f'{self.get_task_type_display()} - {self.name}'

class TaskResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='task_result',
        related_query_name='task_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    score_scaled = models.PositiveIntegerField('Балл (%)', null=True, blank=True)
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('under_review', 'На проверке'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='task_results',
        related_query_name='task_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_result_creators',
        related_query_name='task_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_result_editors',
        related_query_name='task_result_editor'
    )

    class Meta:
        verbose_name = 'Результат работы'
        verbose_name_plural = 'Результаты работы'
        default_permissions = ()
        permissions = (
            ('add_task_result', 'Может добавить результат задачи'),
            ('change_task_result', 'Может изменить результат задачи'),
            ('delete_task_result', 'Может удалить результат задачи'),
            ('view_task_result', 'Может просматривать результат задачи'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class PlanResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='plan_result',
        related_query_name='plan_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='plan_results',
        related_query_name='plan_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='plan_result_creators',
        related_query_name='plan_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='plan_result_editors',
        related_query_name='plan_result_editor'
    )

    class Meta:
        verbose_name = 'Результат плана'
        verbose_name_plural = 'Результаты планов'
        default_permissions = ()
        permissions = (
            ('add_plan_result', 'Может добавить результат плана'),
            ('change_plan_result', 'Может изменить результат плана'),
            ('delete_plan_result', 'Может удалить результат плана'),
            ('view_plan_result', 'Может просматривать результат плана'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class MaterialResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='material_result',
        related_query_name='material_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='material_results',
        related_query_name='material_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='material_result_creators',
        related_query_name='material_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='material_result_editors',
        related_query_name='material_result_editor'
    )

    class Meta:
        verbose_name = 'Результат материала'
        verbose_name_plural = 'Результаты материалов'
        default_permissions = ()
        permissions = (
            ('add_material_result', 'Может добавить результат материала'),
            ('change_material_result', 'Может изменить результат материала'),
            ('delete_material_result', 'Может удалить результат материала'),
            ('view_material_result', 'Может просматривать результат материала'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class NewResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='new_result',
        related_query_name='new_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='new_results',
        related_query_name='new_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='new_result_creators',
        related_query_name='new_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='new_result_editors',
        related_query_name='new_result_editor'
    )

    class Meta:
        verbose_name = 'Результат новости'
        verbose_name_plural = 'Результаты новостей'
        default_permissions = ()
        permissions = (
            ('add_new_result', 'Может добавить результат новости'),
            ('change_new_result', 'Может изменить результат новости'),
            ('delete_new_result', 'Может удалить результат новости'),
            ('view_new_result', 'Может просматривать результат новости'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class CourseResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='course_result',
        related_query_name='course_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    progress = models.TextField(verbose_name='Прогресс', default="{}")
    score_scaled = models.PositiveIntegerField('Балл (%)', null=True, blank=True)
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='course_results',
        related_query_name='course_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='course_result_creators',
        related_query_name='course_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='course_result_editors',
        related_query_name='course_result_editor'
    )

    class Meta:
        verbose_name = 'Результат курса'
        verbose_name_plural = 'Результаты курсов'
        default_permissions = ()
        permissions = (
            ('add_course_result', 'Может добавить результат курса'),
            ('change_course_result', 'Может изменить результат курса'),
            ('delete_course_result', 'Может удалить результат курса'),
            ('view_course_result', 'Может просматривать результат курса'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class EventResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='event_result',
        related_query_name='event_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    confirmed = models.BooleanField('Подтвердил участие', default=False)
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='event_results',
        related_query_name='event_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_result_creators',
        related_query_name='event_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_result_editors',
        related_query_name='event_result_editor'
    )

    class Meta:
        verbose_name = 'Результат мероприятия'
        verbose_name_plural = 'Результаты мероприятия'
        default_permissions = ()
        permissions = (
            ('add_event_result', 'Может добавить мероприятие'),
            ('change_event_result', 'Может изменить мероприятие'),
            ('delete_event_result', 'Может удалить мероприятие'),
            ('view_event_result', 'Может просматривать мероприятие'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class TestResult(models.Model):
    task = models.OneToOneField(
        Task,
        related_name='test_result',
        related_query_name='test_result',
        verbose_name='Задача',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    score_scaled = models.PositiveIntegerField('Балл (%)', default=0)
    score = models.IntegerField(verbose_name='Балл', default=0)
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    attempts = models.PositiveIntegerField(verbose_name='Попытки', default=0)
    finished = models.BooleanField('Окончен', default=False)
    outcome = models.ForeignKey(
        'ControlElement',
        related_name='test_results',
        related_query_name='test_result',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_result_creators',
        related_query_name='test_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_result_editors',
        related_query_name='test_result_editor'
    )

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        default_permissions = ()
        permissions = (
            ('add_test_result', 'Может добавить результат теста'),
            ('change_test_result', 'Может изменить результат теста'),
            ('delete_test_result', 'Может удалить результат теста'),
            ('view_test_result', 'Может просматривать результат теста'),
        )

    def __str__(self):
        return f'{self.task} - {self.get_status_display()}'

class TestAttempt(models.Model):
    test_result = models.ForeignKey(
        TestResult,
        related_name='test_attempts',
        related_query_name='test_attempt',
        verbose_name='Тест',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField(verbose_name='Номер')
    score_scaled = models.PositiveIntegerField('Балл (%)', default=0)
    score = models.IntegerField(verbose_name='Балл', default=0)
    STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='waiting')
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    plan_end_time = models.DateTimeField('Конец', null=True, blank=True)
    question_sorting = models.TextField(verbose_name='Сортировка вопросов',  default='[]')
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_attempt_creators',
        related_query_name='test_attempt_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_attempt_editors',
        related_query_name='test_attempt_editor'
    )

    class Meta:
        verbose_name = 'Попытка теста'
        verbose_name_plural = 'Попытка теста'
        default_permissions = ()
        permissions = (
            ('add_test_attempt', 'Может добавить попытку теста'),
            ('change_test_attempt', 'Может изменить попытку теста'),
            ('delete_test_attempt', 'Может удалить попытку теста'),
            ('view_test_attempt', 'Может просматривать попытку теста'),
        )

    def __str__(self):
        return f'{self.test_result.task.test.name} - {self.number} - {self.get_status_display()}'

class QuestionResult(models.Model):
    test_attempt = models.ForeignKey(
        TestAttempt,
        related_name='question_results',
        related_query_name='question_result',
        verbose_name='Попытка теста',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='question_results',
        related_query_name='question_result',
        verbose_name='Вопрос',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(verbose_name='Балл', default=0)
    STATUSES = [
        #('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='assigned')
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='question_result_creators',
        related_query_name='question_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='question_result_editors',
        related_query_name='question_result_editor'
    )

    class Meta:
        verbose_name = 'Результат вопроса'
        verbose_name_plural = 'Результаты вопросов'
        default_permissions = ()
        permissions = (
            ('add_question_result', 'Может добавить результат вопроса'),
            ('change_question_result', 'Может изменить результат вопроса'),
            ('delete_question_result', 'Может удалить результат вопроса'),
            ('view_question_result', 'Может просматривать результат вопроса'),
        )

    def __str__(self):
        return f'{self.question.text} | {self.get_status_display()}'

class AnswerResult(models.Model):
    question_result = models.ForeignKey(
        QuestionResult,
        related_name='answer_results',
        related_query_name='answer_result',
        verbose_name='Результат вопроса',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        Answer,
        related_name='answer_results',
        related_query_name='answer_result',
        verbose_name='Ответ',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    selected_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)
    selected_position = models.PositiveIntegerField(verbose_name='Правильная позиция', null=True, blank=True)
    selected_text_input = models.CharField(verbose_name='Правильный ответ', max_length=255, null=True, blank=True)
    selected_numeric_input = models.IntegerField(verbose_name='Правильный ответ', null=True, blank=True)
    selected_relevant_point = models.ForeignKey(
        RelevantPoint,
        verbose_name='Соответствующий пункт',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='answers_results',
        related_query_name='answers_result'
    )
    score = models.IntegerField(verbose_name='Балл', default=0)
    STATUSES = [
        #('waiting', 'В ожидании'),
        ('assigned', 'Назначено'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('failed', 'Провалено'),
        ('canceled', 'Отменено'),
    ]
    status = models.CharField('Статус', max_length=50, choices=STATUSES, default='assigned')
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    end_time = models.DateTimeField('Конец', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='answer_result_creators',
        related_query_name='answer_result_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='answer_result_editors',
        related_query_name='answer_result_editor'
    )

    class Meta:
        verbose_name = 'Результат ответа'
        verbose_name_plural = 'Результаты ответов'
        default_permissions = ()
        permissions = (
            ('add_answer_result', 'Может добавить результат ответа'),
            ('change_answer_result', 'Может изменить результат ответа'),
            ('delete_answer_result', 'Может удалить результат ответа'),
            ('view_answer_result', 'Может просматривать результат ответа'),
        )

    def __str__(self):
        return f'{self.answer.text} | {self.get_status_display()}'

class TaskTemplateAssignment(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    task_template = models.ForeignKey(
        TaskTemplate,
        related_name='task_template_assignments',
        related_query_name='task_template_assignment',
        verbose_name='Шаблон задачи',
        on_delete=models.CASCADE
    )
    INTERACTION_TYPES = [
        ('selected', 'Выбранное взаимодействие'),
        ('last', 'Последнее взаимодействие исполнителя'),
        ('new', 'Новое взаимодействие исполнителя'),
    ]
    interaction_type = models.CharField(
        'Тип взаимодействия',
        max_length=50,
        choices=INTERACTION_TYPES,
        null = True,
        blank = True
    )
    interaction = models.ForeignKey(
        Interaction,
        verbose_name='Взаимодействие',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_template_assignments',
        related_query_name='task_template_assignment'
    )
    EXECUTOR_TYPES = [
        ('selected', 'Выбранному исполнителю'),
        ('group', 'Группе исполнителей'),
        ('none', 'Без исполнителей'),
    ]
    executor_type = models.CharField('Тип исполнителя', max_length=50, choices=EXECUTOR_TYPES, null=True, blank=True)
    executor = models.ForeignKey(
        Account,
        related_name='task_template_assignment_individual_executors',
        related_query_name='task_template_assignment_individual_executor',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    executor_group = models.ForeignKey(
        AccountsGroup,
        related_name='task_template_assignment_executors',
        related_query_name='task_template_assignment_executor',
        verbose_name='Группа исполнителей',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    manager_control = models.BooleanField('Контроль руководителей', default=False)
    controller_group = models.ForeignKey(
        AccountsGroup,
        related_name='task_template_assignment_controllers',
        related_query_name='task_template_assignment_controller',
        verbose_name='Группа контролеров',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    observer_group = models.ForeignKey(
        AccountsGroup,
        related_name='task_template_assignment_observers',
        related_query_name='task_template_assignment_observer',
        verbose_name='Группа наблюдателей',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    planned_start = models.DateTimeField('Начало по плану', null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='task_template_assignments',
        related_query_name='task_template_assignment'
    )
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    self_assignment = models.BooleanField('Самоназначение', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_template_assignment_creators',
        related_query_name='task_template_assignment_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='task_template_assignment_editors',
        related_query_name='task_template_assignment_editor'
    )

    class Meta:
        verbose_name = 'Назначение шаблона задачи'
        verbose_name_plural = 'Назначения шаблонов задач'
        default_permissions = ()
        permissions = (
            ('add_task_template_assignment', 'Может добавить назначение шаблона задачи'),
            ('change_task_template_assignment', 'Может изменить назначение шаблона задачи'),
            ('delete_task_template_assignment', 'Может удалить назначение шаблона задачи'),
            ('view_task_template_assignment', 'Может просматривать назначение шаблона задачи'),
        )

    def __str__(self):
        return f'{self.task_template} - {self.executor_group if self.executor_group else self.executor}'

class Queue(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='queues',
        related_query_name='queue'
    )
    auto_assignment = models.BooleanField('Автоназначение исполнителя', default=False)
    last_executor_idx = models.IntegerField('Индекс последнего исполнителя', default=0)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_creators',
        related_query_name='queue_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_editors',
        related_query_name='queue_editor'
    )

    class Meta:
        verbose_name = 'Очередь'
        verbose_name_plural = 'Очереди'
        default_permissions = ()
        permissions = (
            ('add_queue', 'Может добавить очередь'),
            ('change_queue', 'Может изменить очередь'),
            ('delete_queue', 'Может удалить очередь'),
            ('view_queue', 'Может просматривать очередь'),
        )

    def __str__(self):
        return self.name

class QueueExecutor(models.Model):
    queue = models.ForeignKey(
        Queue,
        related_name='queue_executors',
        related_query_name='queue_executor',
        verbose_name='Очередь',
        on_delete=models.CASCADE
    )
    executor = models.ForeignKey(
        Account,
        related_name='queue_executors',
        related_query_name='queue_executor',
        verbose_name='Аккаунт',
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField(verbose_name='Пункт')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_executor_creators',
        related_query_name='queue_executor_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_executor_editors',
        related_query_name='queue_executor_editor'
    )

    class Meta:
        verbose_name = 'Исполнитель в очереди'
        verbose_name_plural = 'Исполнители в очереди'
        default_permissions = ()
        permissions = (
            ('add_queue_executor', 'Может добавить исполнителя в очередь'),
            ('change_queue_executor', 'Может изменить исполнителя в очереди'),
            ('delete_queue_executor', 'Может удалить исполнителя из очереди'),
            ('view_queue_executor', 'Может просматривать исполнителя в очереди'),
        )

    def __str__(self):
        return f'{self.queue} - {self.executor}'

class QueueTask(models.Model):
    queue = models.ForeignKey(
        Queue,
        related_name='queue_tasks',
        related_query_name='queue_task',
        verbose_name='Очередь',
        on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task,
        related_name='queue_tasks',
        related_query_name='queue_task',
        verbose_name='Задача',
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField(verbose_name='Пункт')
    executor = models.ForeignKey(
        Account,
        related_name='assigned_queue_tasks',
        related_query_name='assigned_queue_task',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_task_creators',
        related_query_name='queue_task_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='queue_task_editors',
        related_query_name='queue_task_editor'
    )

    class Meta:
        verbose_name = 'Задача в очереди'
        verbose_name_plural = 'Задачи в очереди'
        default_permissions = ()
        permissions = (
            ('add_queue_task', 'Может добавить задачу в очередь'),
            ('change_queue_task', 'Может изменить задачу в очереди'),
            ('delete_queue_task', 'Может удалить задачу из очереди'),
            ('view_queue_task', 'Может просматривать задачу в очереди'),
        )

    def __str__(self):
        return f'{self.queue} - {self.task}'


class ControlElement(models.Model):
    TYPES_OF_WORK = [
        ('task_outcome', 'Результат задачи'),
        ('trigger', 'Триггер'),
    ]
    type_of_work = models.CharField(
        verbose_name='Тип работы',
        max_length=50,
        choices=TYPES_OF_WORK,
        null=True, blank=True,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='control_elements',
        related_query_name='control_element'
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    task_template = models.ForeignKey(
        TaskTemplate,
        verbose_name='Шаблон задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_template_control_elements',
        related_query_name='task_template_control_element'
    )
    repeat = models.BooleanField('Многократное срабатывание', default=False)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='control_element_creators',
        related_query_name='control_element_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='control_element_editors',
        related_query_name='control_element_editor'
    )

    class Meta:
        verbose_name = 'Управляющий элемент'
        verbose_name_plural = 'Управляющие элементы'
        default_permissions = ()
        permissions = (
            ('add_control_element', 'Может добавить управляющий элемент'),
            ('change_control_element', 'Может изменить управляющий элемент'),
            ('delete_control_element', 'Может удалить управляющий элемент'),
            ('view_control_element', 'Может просматривать управляющий элемент'),
        )

    def __str__(self):
        return f'{self.name}'
        #return f'{self.get_type_of_work_dysplay} - {self.name}'

class ControlElementActivation(models.Model):
    control_element = models.ForeignKey(
        ControlElement,
        related_name='activations',
        related_query_name='activation',
        verbose_name='Управляющий элемент',
        on_delete=models.CASCADE
    )
    interaction = models.ForeignKey(
        Interaction,
        related_name='control_element_activations',
        related_query_name='control_element_activation',
        verbose_name='Взаимодействие',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)

    class Meta:
        verbose_name = 'Срабатывание управляющего элемента'
        verbose_name_plural = 'Срабатывания управляющих элементов'
        default_permissions = ()
        permissions = (
            ('add_control_element_activation', 'Может добавить срабатывание управляющего элемента'),
            ('change_control_element_activation', 'Может изменить срабатывание управляющего элемента'),
            ('delete_control_element_activation', 'Может удалить срабатывание управляющего элемента'),
            ('view_control_element_activation', 'Может просматривать срабатывание управляющего элемента'),
        )

    def __str__(self):
        return f'{self.control_element} - {self.interaction}'

class ControlElementEvent(models.Model):
    control_element = models.ForeignKey(
        ControlElement,
        related_name='events',
        related_query_name='event',
        verbose_name='Управляющий элемент',
        on_delete=models.CASCADE
    )
    EVENT_TYPES = [
        #('client_created', 'Клиент создан'),
        #('task_created', 'Задача создана'),
        ('account_created', 'Аккаунт создан'),
        ('child_task_status_changed', 'Изменился статус дочерней задачи'),
        ('task_deadline', 'Истек срок задачи'),
        ('task_status_changed', 'Изменился статус задачи'),
        ('task_outcome_changed', 'Изменился итог задачи'),
        ('trigger_fired', 'Сработал триггер'),
        ('periodic_event', 'Периодическое событие'),
    ]
    event_type = models.CharField('Событие', max_length=50, choices=EVENT_TYPES)
    task_template = models.ForeignKey(
        TaskTemplate,
        related_name='events',
        related_query_name='event',
        verbose_name='Шаблон задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    fired_trigger = models.ForeignKey(
        ControlElement,
        related_name='fired_trigger_events',
        related_query_name='fired_trigger_event',
        verbose_name='Сработавший триггер',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    PERIODS = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    period = models.CharField('Событие', max_length=50, choices=PERIODS, null=True, blank=True)
    start_time = models.DateTimeField('Начало', null=True, blank=True)
    work_time = models.DateTimeField('Время срабатывания', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_creators',
        related_query_name='event_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='event_editors',
        related_query_name='event_editor'
    )

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        default_permissions = ()
        permissions = (
            ('add_control_element_event', 'Может добавить событие управляющего элемента'),
            ('change_control_element_event', 'Может изменить событие управляющего элемента'),
            ('delete_control_element_event', 'Может удалить событие управляющего элемента'),
            ('view_control_element_event', 'Может просматривать событие управляющего элемента'),
        )

    def __str__(self):
        if self.event_type == 'task_created':
            return f'{self.control_element} - {self.get_event_type_display()} - {self.task_template}'
        elif self.event_type == 'task_status_changed':
            return f'{self.control_element} - {self.get_event_type_display()} - {self.task_template}'
        elif self.event_type == 'task_outcome_changed':
            return f'{self.control_element} - {self.get_event_type_display()} - {self.task_template}'
        elif self.event_type == 'trigger_fired':
            return f'{self.control_element} - {self.get_event_type_display()} - {self.fired_trigger}'
        elif self.event_type == 'periodic_event':
            return f'{self.control_element} - {self.get_event_type_display()} - {self.task_template} - {self.get_period_display()} - {self.start_time.strftime("%d.%m.%Y %H:%M")}'
        return f'Неизвестный тип события'

class ControlElementCondition(models.Model):
    control_element = models.ForeignKey(
        ControlElement,
        related_name='conditions',
        related_query_name='condition',
        verbose_name='Управляющий элемент',
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField('Пункт', null=True, blank=True)
    LOGIC_OPERATORS = [
        ('and', 'И'),
        ('or', 'ИЛИ'),
    ]
    logic_operator = models.CharField('Логический оператор', max_length=50, null=True, blank=True, choices=LOGIC_OPERATORS)
    CONDITION_TYPES = [
        ('task_exists', 'Задача назначалась'),
        ('child_tasks_status', 'Статус дочерних задач'),
        ('task_status', 'Статус задачи'),
        ('task_outcome', 'Итог задачи'),
        ('days_worked', 'Стаж аккаунта взаимодействия'),
    ]
    condition_type = models.CharField('Условие', max_length=50, choices=CONDITION_TYPES)
    task_template = models.ForeignKey(
        TaskTemplate,
        related_name='conditions',
        related_query_name='condition',
        verbose_name='Шаблон задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    boolean_operator = models.BooleanField('Оператор сравнения', default=False)
    COMPARISON_OPERATORS = [
        ('equal', 'Равно'),
        ('not_equal', 'Не равно'),
    ]
    comparison_operator = models.CharField('Оператор сравнения', max_length=50, choices=COMPARISON_OPERATORS, null=True, blank=True)
    ORDER_OPERATORS = [
        ('gte', 'Больше или равно'),
        ('lte', 'Меньше или равно'),
    ]
    order_operator = models.CharField('Оператор сравнения', max_length=50, choices=ORDER_OPERATORS, null=True, blank=True)
    TASK_STATUSES = [
        ('waiting', 'В ожидании'),
        ('assigned', 'Назначена'),
        ('in_progress', 'В процессе'),
        ('under_review', 'На проверке'),
        ('completed', 'Выполнена'),
        ('failed', 'Провалена'),
        ('canceled', 'Отменена'),
    ]
    task_status = models.CharField('Статус задачи', max_length=50, choices=TASK_STATUSES, null=True, blank=True)
    task_outcome = models.ForeignKey(
        ControlElement,
        related_name='task_outcome_conditions',
        related_query_name='task_outcome_condition',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    TARGET_TASKS = [
        ('current', 'В рамках текущего взаимодействия'),
        ('all', 'В рамках всех взаимодействий'),
    ]
    target_task = models.CharField('Целевая задача', max_length=50, choices=TARGET_TASKS, null=True, blank=True)
    days_worked = models.PositiveIntegerField(
        verbose_name='Дни стажа',
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='conditions_creators',
        related_query_name='condition_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='conditions_editors',
        related_query_name='condition_editor'
    )

    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'
        default_permissions = ()
        permissions = (
            ('add_control_element_condition', 'Может добавить условие для управляющего элемента'),
            ('change_control_element_condition', 'Может изменить условие для управляющего элемента'),
            ('delete_control_element_condition', 'Может удалить условие для управляющего элемента'),
            ('view_control_element_condition', 'Может просматривать условие для управляющего элемента'),
        )

    def __str__(self):
        if self.condition_type == 'task_not_exists':
            return f'{self.control_element} - {self.get_condition_type_display()} - {self.task_template.name}'
        elif self.condition_type == 'child_tasks_status':
            return f'{self.control_element} - {self.get_condition_type_display()} - {self.task_template.name} - {self.get_comparison_operator_display()} - {self.get_task_status_display()}'
        elif self.condition_type == 'task_status':
            return f'{self.control_element} - {self.get_condition_type_display()} - {self.task_template.name} - {self.get_comparison_operator_display()} - {self.get_task_status_display()}'
        elif self.condition_type == 'task_outcome':
            return f'{self.control_element} - {self.get_condition_type_display()} - {self.task_template.name} - {self.get_comparison_operator_display()} - {self.task_outcome}'
        elif self.condition_type == 'days_worked':
            return f'{self.control_element} - {self.get_condition_type_display()} - {self.get_order_operator_display()} - {self.days_worked}'
        return f'Неизвестный тип условия'

class ControlElementAction(models.Model):
    control_element = models.ForeignKey(
        ControlElement,
        related_name='actions',
        related_query_name='action',
        verbose_name='Управляющий элемент',
        on_delete=models.CASCADE
    )
    item = models.PositiveIntegerField('Пункт', null=True, blank=True)
    ACTIONS_TYPES = [
        ('change_task_status', 'Изменить статус задачи'),
        ('change_task_outcome', 'Изменить итог задачи'),
        ('assign_task', 'Назначить задачу'),
        ('add_task_to_queue', 'Добавить задачу в очередь'),
        ('new_interaction', 'Новое взаимодействие'),
        ('add_to_group', 'Добавить аккаунт взаимодействия в группу'),
        ('remove_from_group', 'Удалить аккаунт взаимодействия из группы'),
    ]
    action_type = models.CharField('Действия', max_length=50, choices=ACTIONS_TYPES, null=True, blank=True)
    task_template = models.ForeignKey(
        TaskTemplate,
        related_name='actions',
        related_query_name='action',
        verbose_name='Шаблон задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    task_status = models.CharField('Статус задачи', max_length=50, choices=ControlElementCondition.TASK_STATUSES, null=True, blank=True)
    task_outcome = models.ForeignKey(
        ControlElement,
        related_name='task_outcome_actions',
        related_query_name='task_outcome_action',
        verbose_name='Итог задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    TARGET_TASKS = [
        ('current', 'В рамках текущего взаимодействия'),
        ('all', 'В рамках всех взаимодействий'),
    ]
    target_task = models.CharField('Целевая задача', max_length=50, choices=TARGET_TASKS, null=True, blank=True)
    target_group = models.ForeignKey(
        AccountsGroup,
        related_name='target_groups',
        related_query_name='target_group',
        verbose_name='Целевая группа',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    TARGET_INTERACTIONS = [
        ('current', 'Текущее'),
        ('last', 'Последнее'),
    ]
    target_interaction = models.CharField('Целевое взаимодействие', max_length=50, choices=TARGET_INTERACTIONS, null=True, blank=True)
    EXECUTORS_TYPES = [
        ('current_executor', 'Текущий исполнитель'),
        ('selected_executor', 'Выбранный исполнитель'),
        ('none', 'Без исполнителя'),
    ]
    executor_type = models.CharField('Тип исполнителя', max_length=50, choices=EXECUTORS_TYPES, null=True, blank=True)
    executor = models.ForeignKey(
        Account,
        related_name='assignment_executor_actions',
        related_query_name='assignment_executor_action',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    manager_control = models.BooleanField('Контроль руководителей', default=False)
    controller_group = models.ForeignKey(
        AccountsGroup,
        related_name='assignment_controller_group_actions',
        related_query_name='assignment_controller_group_action',
        verbose_name='Группа контролеров',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    observer_group = models.ForeignKey(
        AccountsGroup,
        related_name='assignment_observer_group_actions',
        related_query_name='assignment_observer_group_action',
        verbose_name='Группа наблюдателей',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    DELAY_TYPES = [
        ('minutes', 'Минуты'),
        ('hours', 'Часы'),
        ('days', 'Дни'),
        ('none', 'Без задержки'),
    ]
    delay_type = models.CharField('Тип задержки', max_length=50, choices=DELAY_TYPES, null=True, blank=True)
    delay_value = models.PositiveIntegerField('Задержка', null=True, blank=True)
    queue = models.ForeignKey(
        Queue,
        related_name='queued_actions',
        related_query_name='queued_action',
        verbose_name='Очередь',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='actions_creators',
        related_query_name='action_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='actions_editors',
        related_query_name='action_editor'
    )

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        default_permissions = ()
        permissions = (
            ('add_control_element_action', 'Может добавить действие'),
            ('change_control_element_action', 'Может изменить действие'),
            ('delete_control_element_action', 'Может удалить действие'),
            ('view_control_element_action', 'Может просматривать действие'),
        )

    def __str__(self):
        if self.action_type == 'change_task_status':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.task_template} - {self.get_task_status_display()}'
        elif self.action_type == 'change_task_outcome':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.task_template} - {self.task_outcome}'
        elif self.action_type == 'assign_task':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.task_template} - {self.get_executor_type_display()}'
        elif self.action_type == 'add_task_to_queue':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.task_template} - {self.queue}'
        elif self.action_type == 'add_to_group':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.target_group}'
        elif self.action_type == 'remove_from_group':
            return f'{self.control_element} - {self.get_action_type_display()} -  {self.target_group}'
        elif self.action_type == 'new_interaction':
            return f'{self.control_element} - {self.get_action_type_display()}'
        return f'Неизвестный тип действия'
