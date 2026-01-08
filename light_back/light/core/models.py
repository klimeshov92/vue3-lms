from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract

'''
Аккаунт пользователя с дополнительными полями.
Поля наследуемые от AbstractUser:
- username;
- password;
- email;
- first_name;
- last_name;
- is_active;
- groups;
- user_permissions;
- is_staff;
- is_superuser;
- last_login;
- date_joined.
'''
class Account(AbstractUser):
    mdm_id = models.CharField(verbose_name='MDM ID аккаунта', unique=True, null=True, blank=True, max_length=32)
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='account_avatars/')
    self_registration = models.BooleanField(verbose_name='Самостоятельная регистрация', default=False)
    legal_agree = models.BooleanField(default=False, verbose_name="Согласие с пользовательским соглашением")
    policy_agree = models.BooleanField(default=False, verbose_name="Согласие с политикой конфиденциальности")
    email_confirmed = models.BooleanField(default=False, verbose_name="Подтверждение электронной почты")
    middle_name = models.CharField(verbose_name='Отчество', null=True, blank=True, max_length=255, db_index=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        'self',
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='account_creators',
        related_query_name='account_creator'
    )
    editor = models.ForeignKey(
        'self',
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='account_editors',
        related_query_name='account_editor'
    )

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        default_permissions = ()
        permissions = (
            ('add_account', 'Может добавить аккаунт'),
            ('change_account', 'Может изменить аккаунт'),
            ('delete_account', 'Может удалить аккаунт'),
            ('view_account', 'Может просматривать аккаунт'),
            ('change_self_account', 'Может изменить свой аккаунт'),
        )

    def __str__(self):
        positions_subdivisions_organizations_list = [
            f"{placement.position.name} - {placement.position.subdivision.name} - {placement.position.subdivision.organization.legal_name}"
            for placement in self.placements.filter(end_date=None)
        ]
        positions_subdivisions_organizations_str = ' | '.join(positions_subdivisions_organizations_list)
        if self.last_name and self.first_name and self.placements.exists():
            return f'{self.username} - {self.last_name} {self.first_name} - ({positions_subdivisions_organizations_str})'
        elif self.last_name and self.first_name:
            return f'{self.username} - {self.last_name} {self.first_name}'
        else:
            return f'{self.username}'

class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    parent_category = models.ForeignKey(
        'self',
        verbose_name='Родительская категория',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='categories',
        related_query_name='category'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='categories_creators',
        related_query_name='categories_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='category_editors',
        related_query_name='category_editor'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_permissions = ()
        permissions = (
            ('add_category', 'Может добавить категорию'),
            ('change_category', 'Может изменить категорию'),
            ('delete_category', 'Может удалить категорию'),
            ('view_category', 'Может просматривать категорию'),
        )

    # Получение родительских категорий по цепочке.
    def get_parents_chain(self):
        if self.parent_category:
            return f'{self.parent_category.get_parents_chain()} - {self.name}'
        else:
            return self.name

    # Строкове представление.
    def __str__(self):
        return f'{self.get_parents_chain()}'


class Client(models.Model):
    mdm_id = models.CharField(verbose_name='MDM ID аккаунта', unique=True, null=True, blank=True, max_length=32)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='clients',
        related_query_name='client'
    )
    name = models.CharField('Название', max_length=255)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    account = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Аккаунт клиента',
        related_name='clients',
        related_query_name='client'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='client_creators',
        related_query_name='client_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='client_editors',
        related_query_name='client_editor'
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        default_permissions = ()
        permissions = (
            ('add_client', 'Может добавить клиента'),
            ('change_client', 'Может изменить клиента'),
            ('delete_client', 'Может удалить клиента'),
            ('view_client', 'Может просматривать клиента'),
        )

    def __str__(self):
        return f'{self.name}'

class AccountsGroup(Group):
    TYPES = [
        ('custom', 'Пользовательская'),
        ('system', 'Системная'),
        ('organization', 'Организация'),
        ('subdivision', 'Подразделение'),
        ('position', 'Должность'),
        ('task_co_executors', 'Соисполнители задачи'),
        ('task_controllers', 'Контролеры задачи'),
        ('task_observers', 'Наблюдатели задачи'),
        ('assignment', 'Назначение'),
        ('excel_import', 'Импорт из Excel'),
        ('api_import', 'Импорт по API'),
        ('event_participants', 'Участники мероприятия'),
        ('event_responsible', 'Ответственные мероприятия'),
    ]
    type = models.CharField(max_length=255, choices=TYPES, default='custom', verbose_name='Тип')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='groups',
        related_query_name='group'
    )
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_creators',
        related_query_name='group_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_editors',
        related_query_name='group_editor'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        default_permissions = ()
        permissions = (
            ('add_accounts_group', 'Может добавить группу'),
            ('change_accounts_group', 'Может изменить группу'),
            ('delete_accounts_group', 'Может удалить группу'),
            ('view_accounts_group', 'Может просматривать группу'),
        )

    def __str__(self):
        # Имя в зависимости от связанного объекта.
        if hasattr(self, 'organization'):
            return f'{self.name}'
        elif hasattr(self, 'subdivision'):
            return f'{self.name} - {self.subdivision.organization.legal_name}'
        elif hasattr(self, 'position'):
            return f'{self.name} - {self.position.subdivision.name} - {self.position.subdivision.organization.legal_name}'
        else:
            return f' {self.name}'

class AccountsGroupObjectPermission(GroupObjectPermissionAbstract):
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='accounts_group_object_permissions_creators',
        related_query_name='accounts_group_object_permissions_creator'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    class Meta:
        verbose_name = 'Права группы на объект'
        verbose_name_plural = 'Права группы на объекты'
        default_permissions = ()  # Отключаем стандартные права
        permissions = (
            ('add_accounts_group_object_permission', 'Может добавить права группы на объект'),
            ('change_accounts_group_object_permission', 'Может изменить права группы на объект'),
            ('delete_accounts_group_object_permission', 'Может удалить права группы на объект'),
            ('view_accounts_group_object_permission', 'Может просматривать права группы на объект'),
        )

    def __str__(self):
        return f'{self.group} - {self.permission}'

class AccountObjectPermission(UserObjectPermissionAbstract):
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='account_object_permissions_creators',
        related_query_name='account_object_permissions_creator'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    class Meta:
        verbose_name = 'Права сотрудника на объект'
        verbose_name_plural = 'Права сотрудника на объекты'
        default_permissions = ()  # Отключаем стандартные права
        permissions = (
            ('add_account_object_permission', 'Может добавить права сотрудника на объект'),
            ('change_account_object_permission', 'Может изменить права сотрудника на объект'),
            ('delete_account_object_permission', 'Может удалить права сотрудника на объект'),
            ('view_account_object_permission', 'Может просматривать права сотрудника на объект'),
        )

    def __str__(self):
        return f'{self.user} - {self.permission}'

class Organization(models.Model):
    mdm_id = models.CharField(verbose_name='MDM ID организации', unique=True, null=True, blank=True, max_length=32)
    legal_name = models.CharField(verbose_name='Юридическое название', max_length=255, db_index=True)
    tin = models.CharField(verbose_name='ИНН организации', max_length=32)
    group = models.OneToOneField(
        AccountsGroup,
        verbose_name='Группа прав',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='organization',
        related_query_name='organization'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='organizations_creators',
        related_query_name='organizations_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='organization_editors',
        related_query_name='organization_editor'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        default_permissions = ()  # Отключаем стандартные права
        permissions = (
            ('add_organization', 'Может добавить организацию'),
            ('change_organization', 'Может изменить организацию'),
            ('delete_organization', 'Может удалить организацию'),
            ('view_organization', 'Может просматривать организацию'),
        )

    def __str__(self):
        return f'{self.legal_name}'

class Subdivision(models.Model):
    mdm_id = models.CharField(verbose_name='MDM ID подразделения', unique=True, null=True, blank=True, max_length=32)
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='subdivisions',
        related_query_name='subdivision'
    )
    parent_subdivision = models.ForeignKey(
        'self',
        verbose_name='Главное подразделение',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subdivisions',
        related_query_name='subdivision'
    )
    group = models.OneToOneField(
        AccountsGroup,
        verbose_name='Группа прав',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='subdivision',
        related_query_name='subdivision'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subdivisions_creators',
        related_query_name='subdivisions_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subdivision_editors',
        related_query_name='subdivision_editor'
    )

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        default_permissions = ()
        permissions = (
            ('add_subdivision', 'Может добавить подразделение'),
            ('change_subdivision', 'Может изменить подразделение'),
            ('delete_subdivision', 'Может удалить подразделение'),
            ('view_subdivision', 'Может просматривать подразделение'),
        )

    # Строковое представление.
    def __str__(self):
        return f'{self.name} - {self.organization.legal_name}'

class Position(models.Model):
    mdm_id = models.CharField(verbose_name='MDM ID должности', unique=True, null=True, blank=True, max_length=32)
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    subdivision = models.ForeignKey(
        Subdivision,
        verbose_name='Подразделение',
        on_delete=models.CASCADE,
        related_name='positions',
        related_query_name='position'
    )
    group = models.OneToOneField(
        AccountsGroup,
        verbose_name='Группа прав',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='position',
        related_query_name='position'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='positions_creators',
        related_query_name='positions_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='position_editors',
        related_query_name='position_editor'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        default_permissions = ()
        permissions = (
            ('add_position', 'Может добавить должность'),
            ('change_position', 'Может изменить должность'),
            ('delete_position', 'Может удалить должность'),
            ('view_position', 'Может просматривать должность'),
        )

    # Строковое представление.
    def __str__(self):
        return f'{self.name} - {self.subdivision.name} - {self.subdivision.organization.legal_name}'

class Placement(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name='Сотрудник',
        on_delete=models.PROTECT,
        related_name='placements',
        related_query_name='placements'
    )
    position = models.ForeignKey(
        Position,
        verbose_name='Должность',
        on_delete=models.PROTECT,
        related_name='placements',
        related_query_name='placements'
    )
    ROLES = [
        ('employee', 'Сотрудник'),
        ('manager', 'Менеджер'),
    ]
    role = models.CharField(max_length=255, choices=ROLES, default='custom', verbose_name='Тип')
    start_date = models.DateField(verbose_name='Дата начала работы', null=True, blank=True)
    end_date = models.DateField(
        verbose_name='Дата окончания работы',
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создатель',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='placements_creators',
        related_query_name='placements_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='placement_editors',
        related_query_name='placement_editor'
    )

    class Meta:
        verbose_name = 'Назначение на должность'
        verbose_name_plural = 'Назначение на должности'
        default_permissions = ()
        permissions = (
            ('add_placement', 'Может добавить назначение на должность'),
            ('change_placement', 'Может изменить назначение на должность'),
            ('delete_placement', 'Может удалить назначение на должность'),
            ('view_placement', 'Может просматривать назначение на должность'),
        )

    # Строковое представление.
    def __str__(self):
        return f'{self.account.last_name} {self.account.first_name} | ' \
               f'{self.position.name} - {self.position.subdivision.name} - {self.position.subdivision.organization.legal_name}'

class GroupGenerator(models.Model):
    group = models.OneToOneField(
        AccountsGroup,
        verbose_name='Группа прав',
        on_delete=models.CASCADE,
        related_name='generator_group',
        related_query_name='generator_group')
    added_groups = models.ManyToManyField(
        AccountsGroup,
        verbose_name='Добавляемые группы',
        blank=True,
        related_name='added_group_generator_groups',
        related_query_name='added_group_generator_group'
    )
    added_users = models.ManyToManyField(
        Account,
        verbose_name='Добавляемые сотрудники',
        blank=True,
        related_name='added_group_generator_users',
        related_query_name='added_group_generator_user'
    )
    excluded_groups = models.ManyToManyField(
        AccountsGroup,
        verbose_name='Исключаемые группы',
        blank=True,
        related_name='excluded_group_generator_groups',
        related_query_name='excluded_group_generator_group'
    )
    excluded_users = models.ManyToManyField(
        Account,
        verbose_name='Исключаемые сотрудники',
        blank=True,
        related_name='excluded_group_generator_users',
        related_query_name='excluded_group_generator_user'
    )
    days_worked_gte = models.IntegerField(
        verbose_name='Отработано от (дней)',
        null=True,
        blank=True,
        default=0,
        validators=[MinValueValidator(0)]
    )
    days_worked_lte = models.IntegerField(
        verbose_name='Отработано до (дней)',
        null=True,
        blank=True,
        default=90,
        validators=[MinValueValidator(0)]
    )
    autoupdate = models.BooleanField(verbose_name='Автообновление', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_generator_creators',
        related_query_name='group_generator_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_generator_editors',
        related_query_name='group_generator_editor'
    )

    class Meta:
        verbose_name = 'Генератор групп'
        verbose_name_plural = 'Генераторы групп'
        default_permissions = ()  # Отключаем стандартные права
        permissions = (
            ('add_group_generator', 'Может добавить генератор групп'),
            ('change_group_generator', 'Может изменить генератор групп'),
            ('delete_group_generator', 'Может удалить генератор групп'),
            ('view_group_generator', 'Может просматривать генератор групп'),
        )

    def __str__(self):
        return f'{self.group.name}'

class HomePage(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, db_index=True)
    content = models.TextField(verbose_name='Содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='home_page_creators',
        related_query_name='home_page_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='home_page_editors',
        related_query_name='home_page_editor'
    )

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'
        default_permissions = ()
        permissions = (
            ('add_home_page', 'Может добавить главную страницу'),
            ('change_home_page', 'Может изменить главную страницу'),
            ('delete_home_page', 'Может удалить главную страницу'),
            ('view_home_page', 'Может просматривать главную страницу'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.title}'

    # Ограничение одной записью.
    def save(self, *args, **kwargs):
        if not self.pk and HomePage.objects.exists():
            raise ValueError("Может быть только одна главная страница")
        return super().save(*args, **kwargs)

class LegalPage(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, db_index=True)
    content = models.TextField(verbose_name='Содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='legal_page_creators',
        related_query_name='legal_page_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='legal_page_editors',
        related_query_name='legal_page_editor'
    )

    class Meta:
        verbose_name = 'Страница пользовательского соглашения'
        verbose_name_plural = 'Страница пользовательского соглашения'
        default_permissions = ()
        permissions = (
            ('add_legal_page', 'Может добавить страницу пользовательского соглашения'),
            ('change_legal_page', 'Может изменить страницу пользовательского соглашения'),
            ('delete_legal_page', 'Может удалить страницу пользовательского соглашения'),
            ('view_legal_page', 'Может просматривать страницу пользовательского соглашения'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.title}'

    # Ограничение одной записью.
    def save(self, *args, **kwargs):
        if not self.pk and LegalPage.objects.exists():
            raise ValueError("Может быть только одна страница пользовательского соглашения")
        return super().save(*args, **kwargs)

class PolicyPage(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, db_index=True)
    content = models.TextField(verbose_name='Содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='policy_page_creators',
        related_query_name='policy_page_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='policy_page_editors',
        related_query_name='policy_page_editor'
    )

    class Meta:
        verbose_name = 'Страница политики конфиденциальности'
        verbose_name_plural = 'Страница политики конфиденциальности'
        default_permissions = ()
        permissions = (
            ('add_policy_page', 'Может добавить страницу политики конфиденциальности'),
            ('change_policy_page', 'Может изменить главную политики конфиденциальности'),
            ('delete_policy_page', 'Может удалить главную политики конфиденциальности'),
            ('view_policy_page', 'Может просматривать главную политики конфиденциальности'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.title}'

    # Ограничение одной записью.
    def save(self, *args, **kwargs):
        if not self.pk and PolicyPage.objects.exists():
            raise ValueError("Может быть только одна страница политики конфиденциальности")
        return super().save(*args, **kwargs)