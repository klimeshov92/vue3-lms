from django.db import models

# Create your models here.

from core.models import *

class Material(models.Model):
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True, upload_to='material_avatars/')
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='materials',
        related_query_name='materials',
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
        related_name='material_creators',
        related_query_name='material_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='material_editors',
        related_query_name='material_editor'
    )

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
        default_permissions = ()
        permissions = (
            ('add_material', 'Может добавить материал'),
            ('change_material', 'Может изменить материал'),
            ('delete_material', 'Может удалить материал'),
            ('view_material', 'Может просматривать материал'),
        )

    # Строкове представление.
    def __str__(self):
        return f'{self.name}'
