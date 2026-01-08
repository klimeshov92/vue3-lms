import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from core.models import *
from django.conf import settings
import logging
from asgiref.sync import sync_to_async
from django.utils import timezone
import pytz

logger = logging.getLogger('project')

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        try:

            user = self.scope['user']
            logger.debug(f"Пользователь {user.username} [{user.id})] выполняет подключение")

            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"chat_{self.room_name}"
            logger.debug(f"Подключение к комнате: {self.room_name}, чат: {self.room_group_name}")

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            logger.debug(f"Соединение установлено с WebSocket: {self.channel_name}")

        except Exception as e:
            logger.exception(f"Ошибка при установке соединения с WebSocket: {str(e)}")
            await self.send(text_data=json.dumps({'error': 'Ошибка при подключении к WebSocket'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.debug(f"Отключение от комнаты: {self.room_name}, код: {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')

            if action == 'load_old_messages':
                try:
                    await self.load_old_messages()
                except Exception as e:
                    logger.exception(f"Ошибка в load_old_messages: {e}")
                    await self.send(text_data=json.dumps({'error': 'Ошибка при загрузке сообщений через WebSocket'}))
                return

            if action == 'send_message':
                try:
                    await self.send_messages(data)
                except Exception as e:
                    logger.exception(f"Ошибка в send_messages: {e}")
                    await self.send(text_data=json.dumps({'error': 'Ошибка при отправке сообщения через WebSocket'}))
                return

            if action == 'edit_message':
                try:
                    await self.edit_message(data)
                except Exception as e:
                    logger.exception(f"Ошибка в edit_message: {e}")
                    await self.send(text_data=json.dumps({'error': 'Ошибка при редактировании сообщения через WebSocket'}))
                return

            if action == 'delete_message':
                try:
                    await self.delete_message(data)
                except Exception as e:
                    logger.exception(f"Ошибка в delete_message: {e}")
                    await self.send(text_data=json.dumps({'error': 'Ошибка при удалении сообщения через WebSocket'}))
                return

        except Exception as e:
            logger.exception(f"Ошибка в receive: {e}")
            await self.send(text_data=json.dumps({'error': 'Произошла ошибка, попробуйте позже'}))

    async def load_old_messages(self):
        logger.debug(f"Загрузка старых сообщений комнаты: {self.room_name}")

        def get_message_data_sync(messages):
            return [
                {
                    'id': msg.id,
                    'content': msg.content,
                    'sender': {
                        'id': msg.sender.id,
                        'str': str(msg.sender),
                    },
                    'changed': timezone.localtime(msg.changed).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                }
                for msg in messages
            ]

        chat = await sync_to_async(Chat.objects.get, thread_sensitive=True)(id=self.room_name)
        messages = await sync_to_async(list, thread_sensitive=True)(chat.messages.all().order_by('changed'))
        message_data = await sync_to_async(get_message_data_sync, thread_sensitive=True)(messages)

        await self.send(text_data=json.dumps({'old_messages': message_data}))


    async def send_messages(self, data):
        message_content = data['message']
        user = self.scope['user']
        logger.debug(f"Получено сообщение: {data}")

        chat = await sync_to_async(Chat.objects.get)(id=self.room_name)

        message = Message(
            chat=chat,
            sender=user,
            content=message_content
        )
        await sync_to_async(message.save)()
        logger.debug(f"Сообщение сохранено в чат: {chat.name}")

        changed = timezone.localtime(message.changed)
        changed_at_str = changed.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        def get_sender_data(user):
            return {
                'id': user.id,
                'str': str(user),
            }
        sender = await sync_to_async(get_sender_data)(user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender,
                'changed': changed_at_str,
            }
        )
        logger.debug(f"Сообщение передано подключенным пользователям чата: {self.room_group_name}")

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        changed = event['changed']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'changed': changed,
        }))

    async def edit_message(self, data):
        message_id = data.get('message_id')
        new_content = data.get('new_content')
        user = self.scope['user']
        logger.debug(f"Обновление сообщения: {data}")

        message = await sync_to_async(Message.objects.get)(id=message_id)

        if message.sender_id != user.id:
            logger.debug(f"Пользователь пытался отредактировать чужое сообщение: {user.username}, ID сообщения: {message_id}")
            return

        message.content = new_content
        await sync_to_async(message.save, thread_sensitive=True)()  # Исправленный вызов

        local_time = timezone.localtime(message.changed)
        changed_at_str = local_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "message_edited",
                "message_id": message.id,
                "new_content": new_content,
                "changed": changed_at_str,

            }
        )

        logger.debug(f"Обновление передано подключенным пользователям чата: {self.room_group_name}")

    async def message_edited(self, event):
        await self.send(text_data=json.dumps({
            "action": "message_edited",
            "message_id": event["message_id"],
            "new_content": event["new_content"],
            "changed": event["changed"],
        }))

    async def delete_message(self, data):
        message_id = data.get('message_id')
        user = self.scope['user']
        logger.debug(f"Удаление сообщения: {data}")

        message = await sync_to_async(Message.objects.get)(id=message_id)
        if message.sender_id != user.id:
            logger.debug(f"Пользователь пытался удалить чужое сообщение: {user.username}, ID сообщения: {message_id}")
            return

        await sync_to_async(message.delete)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "message_deleted",
                "message_id": message_id
            }
        )
        logger.debug(f"Обновление передано подключенным пользователям чата: {self.room_group_name}")

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            "action": "message_deleted",
            "message_id": event["message_id"]
        }))


