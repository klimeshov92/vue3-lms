from django.db import models

# Create your models here.

from core.models import *

class File(models.Model):
    FILE_TYPES = [
        ('image', 'Картинка'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        ('document', 'Документ'),
    ]
    file_type = models.CharField(verbose_name='Тип', max_length=255, choices=FILE_TYPES, null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='files',
        related_query_name='files',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    upload_file = models.FileField(verbose_name='Файл', null=True, blank=True, upload_to='files/')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='file_creators',
        related_query_name='file_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='file_editors',
        related_query_name='file_editor'
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        default_permissions = ()
        permissions = (
            ('add_file', 'Может добавить файл'),
            ('change_file', 'Может изменить файл'),
            ('delete_file', 'Может удалить файл'),
            ('view_file', 'Может просматривать файл'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name}'