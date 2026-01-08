from django.db import models

# Create your models here.

from core.models import *

class New(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='new_avatars/')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='news',
        related_query_name='news',
        db_index=True
    )
    name = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    desc = models.TextField(verbose_name='Описание', null=True, blank=True)
    content = models.TextField(verbose_name='Содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', db_index=True)
    changed = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения', db_index=True)
    creator = models.ForeignKey(
        Account,
        verbose_name='Создал',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='new_creators',
        related_query_name='new_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='new_editors',
        related_query_name='new_editor'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        default_permissions = ()
        permissions = (
            ('add_new', 'Может добавить новость'),
            ('change_new', 'Может изменить новость'),
            ('delete_new', 'Может удалить новость'),
            ('view_new', 'Может просматривать новость'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name} - {self.created.strftime("%d.%m.%Y %H:%M")}'