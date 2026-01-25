from django.db import models
from core.models import *
from bpms.models import *

# Create your models here.

class Chat(models.Model):
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='chats',
        related_query_name='chat'
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
        related_name='chat_creators',
        related_query_name='chat_creator'
    )
    editor = models.ForeignKey(
        Account,
        verbose_name='Изменил',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='chat_editors',
        related_query_name='chat_editor'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        default_permissions = ()
        permissions = (
            ('add_chat', 'Может добавить чат'),
            ('change_chat', 'Может изменить чат'),
            ('delete_chat', 'Может удалить чат'),
            ('view_chat', 'Может просматривать чат'),
        )


    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        verbose_name='Чат',
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
        related_name='chat_senders',
        related_query_name='chat_sender'
    )
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        default_permissions = ()
        permissions = (
            ('add_message', 'Может добавить сообщение'),
            ('change_message', 'Может изменить сообщение'),
            ('delete_message', 'Может удалить сообщение'),
            ('view_message', 'Может просматривать сообщение'),
        )

    def __str__(self):
        return f"{self.chat.name} - {self.id}"

