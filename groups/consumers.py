import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import StudyGroup, GroupChatMessage

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if not message:
            return

        new_message = await self.save_message(message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': new_message.content,
                'user': self.user.username,
                'avatar_url': await self.get_avatar_url(self.user)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'avatar_url': event['avatar_url']
        }))

    @database_sync_to_async
    def save_message(self, message):
        group = StudyGroup.objects.get(id=self.group_id)
        return GroupChatMessage.objects.create(group=group, user=self.user, content=message)

    @database_sync_to_async
    def get_avatar_url(self, user):
        if user.profile.avatar:
            return user.profile.avatar.url
        return f"https://ui-avatars.com/api/?name={user.username.replace(' ', '+')}&background=random"