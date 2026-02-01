from django.db import models

# Create your models here.

from core.models import *

class Survey(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='survey_avatars/')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='surveys',
        related_query_name='survey',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    passing_score = models.PositiveIntegerField(verbose_name='Проходной балл', null=True, blank=True)
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение (минут)', null=True, blank=True)
    attempts = models.PositiveIntegerField(verbose_name='Попытки', null=True, blank=True)
    random_sections = models.BooleanField(verbose_name='Случайный порядок секций', default=True)
    random_questions = models.BooleanField(verbose_name='Случайный порядок вопросов', default=True)
    random_answers = models.BooleanField(verbose_name='Случайный порядок ответов', default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_creators',
        related_query_name='survey_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_editors',
        related_query_name='survey_editor'
    )

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        default_permissions = ()
        permissions = (
            ('add_survey', 'Может добавить опрос'),
            ('change_survey', 'Может изменить опрос'),
            ('delete_survey', 'Может удалить опрос'),
            ('view_survey', 'Может просматривать опрос'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name}'

class SurveySection(models.Model):
    item = models.PositiveIntegerField(verbose_name='Пункт')
    test = models.ForeignKey(
        Survey,
        verbose_name='Опрос',
        null=True,
        on_delete=models.CASCADE,
        related_name='survey_sections',
        related_query_name='survey_section',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_section_creators',
        related_query_name='survey_section_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_section_editors',
        related_query_name='survey_section_editor'
    )

    class Meta:
        verbose_name = 'Раздел опроса'
        verbose_name_plural = 'Разделы опроса'
        default_permissions = ()
        permissions = (
            ('add_survey_section', 'Может добавить раздел опроса'),
            ('change_survey_section', 'Может изменить раздел опроса'),
            ('delete_survey_section', 'Может удалить раздел опроса'),
            ('view_survey_section', 'Может просматривать раздел опроса'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.item} - {self.survey}'

class SurveyQuestion(models.Model):
    QUESTION_TYPES = [
        ('single_selection', 'Одиночный выбор'),
        ('multiple_choice', 'Множественный выбор'),
        ('sorting', 'Сортировка'),
        ('text_input', 'Текстовый ввод'),
    ]
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPES, default='', verbose_name='Тип вопроса')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='survey_questions',
        related_query_name='survey_question',
        db_index=True
    )
    manual = models.TextField(verbose_name='Инструкция')
    text = models.TextField(verbose_name='Текст вопроса')
    picture = models.ImageField(verbose_name='Картинка вопроса', null=True, blank=True, upload_to='survey_questions_picture/')
    score = models.IntegerField(verbose_name='Балл', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_question_creators',
        related_query_name='survey_question_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_question_editors',
        related_query_name='survey_question_editor'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        default_permissions = ()
        permissions = (
            ('add_survey_question', 'Может добавить вопрос'),
            ('change_survey_question', 'Может изменить вопрос'),
            ('delete_survey_question', 'Может удалить вопрос'),
            ('view_survey_question', 'Может просматривать вопрос'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.get_question_type_display()} - {self.text}'

class SurveySectionQuestion(models.Model):
    item = models.PositiveIntegerField(verbose_name='Пункт')
    survey_section = models.ForeignKey(
        SurveySection,
        verbose_name='Раздел опроса',
        null=True,
        on_delete=models.CASCADE,
        related_name='survey_section_questions',
        related_query_name='survey_section_question',
        db_index=True
    )
    survey_question = models.ForeignKey(
        SurveyQuestion,
        verbose_name='Вопрос',
        null=True,
        on_delete=models.CASCADE,
        related_name='survey_section_questions',
        related_query_name='survey_section_question',
        db_index=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_section_question_creators',
        related_query_name='survey_section_question_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_section_question_editors',
        related_query_name='survey_section_question_editor'
    )

    class Meta:
        verbose_name = 'Вопрос раздела опроса'
        verbose_name_plural = 'Вопросы раздела опроса'
        default_permissions = ()
        permissions = (
            ('add_survey_section_question', 'Может добавить вопрос раздела опроса'),
            ('change_survey_section_question', 'Может изменить вопрос раздела опроса'),
            ('delete_survey_section_question', 'Может удалить вопрос раздела опроса'),
            ('view_survey_section_question', 'Может просматривать вопрос раздела опроса'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.survey_section} - {self.item} - {self.question}'

class SurveyAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, verbose_name='Вопрос', on_delete=models.CASCADE, related_name='survey_answers', related_query_name='survey_answer', db_index=True)
    item = models.PositiveIntegerField(verbose_name='Позиция в списке', db_index=True)
    text = models.TextField(verbose_name='Текст ответа')
    picture = models.ImageField(verbose_name='Картинка ответа', null=True, blank=True, upload_to='survey_answer_picture/')
    score = models.IntegerField(verbose_name='Балл', default=0)
    correct_answer = models.BooleanField(verbose_name='Правильный ответ', null=True, blank=True)
    correct_item = models.PositiveIntegerField(verbose_name='Правильная позиция', null=True, blank=True)
    correct_text_input = models.CharField(verbose_name='Правильный ответ', max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_answer_creators',
        related_query_name='survey_answer_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_answer_editors',
        related_query_name='survey_answer_editor'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        default_permissions = ()
        permissions = (
            ('add_survey_answer', 'Может добавить ответ'),
            ('change_survey_answer', 'Может изменить ответ'),
            ('delete_survey_answer', 'Может удалить ответ'),
            ('view_survey_answer', 'Может просматривать ответ'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.survey_question} - {self.item} - {self.text}'


