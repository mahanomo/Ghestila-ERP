import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        try:
            self.room = Room.objects.get(name=self.room_name)
        except Room.DoesNotExist:
            self.close()
            return

        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.user.is_authenticated:
            # Add user to room's online list
            self.room.online.add(self.user)

            # Notify others
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )

        # Send the list of online users to the new user
        self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

    def disconnect(self, close_code):
        if self.user and self.user.is_authenticated:
            self.room.online.remove(self.user)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if not self.user or not self.user.is_authenticated:
            return

        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        if message.strip() == "":
            return

        # Save message
        Message.objects.create(user=self.user, room=self.room, content=message)

        # Broadcast message
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))