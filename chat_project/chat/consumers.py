import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q  # Import Q for complex queries

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the receiver's user ID from the URL
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.sender = self.scope['user']

        # Check if the receiver exists
        self.receiver = User.objects.get(id=self.receiver_id)

        # Define the room name using the receiver ID
        self.room_name = f"chat_{self.sender.id}_{self.receiver.id}"
        self.room_group_name = f"chat_{self.room_name}"

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send old messages to the user
        messages = Message.objects.filter(
            (Q(sender=self.sender) & Q(receiver=self.receiver)) |
            (Q(sender=self.receiver) & Q(receiver=self.sender))
        ).order_by('timestamp')

        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.content,
                'sender': message.sender.username,
            }))

    async def disconnect(self, close_code):
        # Leave the group when the WebSocket closes
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Save the message in the database
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content=message_content
        )

        # Send the message to the WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': self.sender.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))