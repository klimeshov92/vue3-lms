from django.db import models

# Create your models here.

from core.models import *

class Test(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='test_avatars/')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='tests',
        related_query_name='test',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    passing_score = models.PositiveIntegerField(verbose_name='Проходной балл', null=True, blank=True)
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение (минут)', null=True, blank=True)
    attempts = models.PositiveIntegerField(verbose_name='Попытки', null=True, blank=True)
    random_questions = models.BooleanField(verbose_name='Случайный порядок вопросов', default=True)
    random_answers = models.BooleanField(verbose_name='Случайный порядок ответов', default=True)
    show_questions_results = models.BooleanField(verbose_name='Показывать результаты вопросов', default=True)
    show_answers_results = models.BooleanField(verbose_name='Показывать результаты ответов', default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_creators',
        related_query_name='test_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_editors',
        related_query_name='test_editor'
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тест'
        default_permissions = ()
        permissions = (
            ('add_test', 'Может добавить тест'),
            ('change_test', 'Может изменить тест'),
            ('delete_test', 'Может удалить тест'),
            ('view_test', 'Может просматривать тест'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name}'

class TestSection(models.Model):
    item = models.PositiveIntegerField(verbose_name='Пункт')
    test = models.ForeignKey(
        Test,
        verbose_name='Тест',
        null=True,
        on_delete=models.CASCADE,
        related_name='test_sections',
        related_query_name='test_section',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    sample_size = models.PositiveIntegerField(verbose_name='Количество вопросов в выборке')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_section_creators',
        related_query_name='test_section_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_section_editors',
        related_query_name='test_section_editor'
    )

    class Meta:
        verbose_name = 'Раздел теста'
        verbose_name_plural = 'Разделы теста'
        default_permissions = ()
        permissions = (
            ('add_test_section', 'Может добавить раздел теста'),
            ('change_test_section', 'Может изменить раздел теста'),
            ('delete_test_section', 'Может удалить раздел теста'),
            ('view_test_section', 'Может просматривать раздел теста'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.item} - {self.test}'

class Question(models.Model):
    QUESTION_TYPES = [
        ('single_selection', 'Одиночный выбор'),
        ('multiple_choice', 'Множественный выбор'),
        ('sorting', 'Сортировка'),
        ('compliance', 'Соотвествие'),
        ('text_input', 'Текстовый ввод'),
        ('numeric_input', 'Числовой ввод'),
    ]
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPES, default='', verbose_name='Тип вопроса')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='questions',
        related_query_name='question',
        db_index=True
    )
    manual = models.TextField(verbose_name='Инструкция')
    text = models.TextField(verbose_name='Текст вопроса')
    picture = models.ImageField(verbose_name='Картинка вопроса', null=True, blank=True, upload_to='questions_picture/')
    score = models.IntegerField(verbose_name='Балл', default=0)
    feedback_for_correct = models.TextField(verbose_name='Обратная связь при правильном ответе', default='Верно!')
    feedback_for_incorrect = models.TextField(verbose_name='Обратная связь при неправильном ответе', default='Неверно!')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='question_creators',
        related_query_name='question_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='question_editors',
        related_query_name='question_editor'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        default_permissions = ()
        permissions = (
            ('add_question', 'Может добавить вопрос'),
            ('change_question', 'Может изменить вопрос'),
            ('delete_question', 'Может удалить вопрос'),
            ('view_question', 'Может просматривать вопрос'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.get_question_type_display()} - {self.text}'

class TestSectionQuestion(models.Model):
    item = models.PositiveIntegerField(verbose_name='Пункт')
    test_section = models.ForeignKey(
        TestSection,
        verbose_name='Раздел теста',
        null=True,
        on_delete=models.CASCADE,
        related_name='test_section_questions',
        related_query_name='test_section_question',
        db_index=True
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        null=True,
        on_delete=models.CASCADE,
        related_name='test_section_questions',
        related_query_name='test_section_question',
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
        related_name='test_section_question_creators',
        related_query_name='test_section_question_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='test_section_question_editors',
        related_query_name='test_section_question_editor'
    )

    class Meta:
        verbose_name = 'Вопрос раздела теста'
        verbose_name_plural = 'Вопросы раздела теста'
        default_permissions = ()
        permissions = (
            ('add_test_section_question', 'Может добавить вопрос раздела теста'),
            ('change_test_section_question', 'Может изменить вопрос раздела теста'),
            ('delete_test_section_question', 'Может удалить вопрос раздела теста'),
            ('view_test_section_question', 'Может просматривать вопрос раздела теста'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.test_section} - {self.item} - {self.question}'

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE, related_name='answers', related_query_name='answer', db_index=True)
    item = models.PositiveIntegerField(verbose_name='Позиция в списке', db_index=True)
    text = models.TextField(verbose_name='Текст ответа')
    picture = models.ImageField(verbose_name='Картинка ответа', null=True, blank=True, upload_to='answer_picture/')
    score = models.IntegerField(verbose_name='Балл', default=0)
    feedback_for_correct = models.TextField(verbose_name='Обратная связь при правильном ответе', default='Верно!')
    feedback_for_incorrect = models.TextField(verbose_name='Обратная связь при неправильном ответе', default='Неверно!')
    correct_answer = models.BooleanField(verbose_name='Правильный ответ', null=True, blank=True)
    correct_item = models.PositiveIntegerField(verbose_name='Правильная позиция', null=True, blank=True)
    correct_text_input = models.CharField(verbose_name='Правильный ответ', max_length=255, null=True, blank=True)
    correct_numeric_input = models.IntegerField(verbose_name='Правильный ответ', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='answer_creators',
        related_query_name='answer_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='answer_editors',
        related_query_name='answer_editor'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        default_permissions = ()
        permissions = (
            ('add_answer', 'Может добавить ответ'),
            ('change_answer', 'Может изменить ответ'),
            ('delete_answer', 'Может удалить ответ'),
            ('view_answer', 'Может просматривать ответ'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.question} - {self.item} - {self.text}'

class RelevantPoint(models.Model):
    answer = models.OneToOneField(
        Answer,
        verbose_name='Ответ',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='relevant_point',
        related_query_name='relevant_point'
    )
    text = models.TextField(verbose_name='Текст пункта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=False)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=False)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='relevant_point_creators',
        related_query_name='relevant_point_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='relevant_point_editors',
        related_query_name='relevant_point_editor'
    )

    class Meta:
        verbose_name = 'Соответствующий пункт'
        verbose_name_plural = 'Соответствующие пункты'
        default_permissions = ()
        permissions = (
            ('add_relevant_point', 'Может добавить соответствующий пункт'),
            ('change_relevant_point', 'Может изменить соответствующий пункт'),
            ('delete_relevant_point', 'Может удалить соответствующий пункт'),
            ('view_relevant_point', 'Может просматривать соответствующий пункт'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.answer} - {self.text}'


