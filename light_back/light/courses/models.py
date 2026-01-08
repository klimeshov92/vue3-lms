from django.db import models

# Create your models here.

from core.models import *

class Course(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='course_avatars/')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='courses',
        related_query_name='courses',
        db_index=True
    )
    CONSTRUCTOR_TYPES = [
        ('ispring', 'Ispring'),
        ('articulate', 'Articulate'),
        ('scroll', 'Scroll'),
    ]
    constructor_type = models.CharField(max_length=255, choices=CONSTRUCTOR_TYPES, verbose_name='Тип', null=True, blank=True)
    upload_file = models.FileField(verbose_name='Файл', upload_to='scorm_packages/', null=True, blank=True)
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='course_creators',
        related_query_name='course_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='course_editors',
        related_query_name='course_editor'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        default_permissions = ()
        permissions = (
            ('add_course', 'Может добавить курс'),
            ('change_course', 'Может изменить курс'),
            ('delete_course', 'Может удалить курс'),
            ('view_course', 'Может просматривать курс'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name}'
