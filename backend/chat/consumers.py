from users.models import User
from users.serializers import UserSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Channel
from .serializers import MessageSerializer
from asgiref.sync import sync_to_async, async_to_sync
import jwt, json, base64

class ChatView(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        if not 'jwt' in data or not 'type' in data:
            await self.close(code=4001)
            return
        token = data['jwt']
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("here3")
            await self.close(code=4001)
            return
        except jwt.DecodeError:
            print("here2")
            await self.close(code=4001)
            return
        
        user = await sync_to_async(User.objects.filter(id=payload['id']).first)()
        if user is None:
            print("here")
            await self.close(code=4001)
            return
        serializer = UserSerializer(user).data
        if data['type'] == 1: #Bulk messages
            self.default_chat, self.chat_name, self.encoded_chat_name = "Main", "Main", await sync_to_async(self.encode)("Main")
            await self.channel_layer.group_add(
                self.default_chat,
                self.channel_name
            )

            messages = await self.get_previous_messages()
            message_serializer = MessageSerializer(messages, many=True)
            serialized_data = await sync_to_async(lambda: message_serializer.data)()
            
            await self.send(text_data=json.dumps({
                'data_type': 'bulk_messages',
                'data': serialized_data
                }))
            return
        if data['type'] == 2: #Chat Creation
            self.chat_name = data['chat_name']
            msg = await self.create_chatroom(self.chat_name, serializer['username'])
            self.encoded_chat_name = await sync_to_async(self.encode)(data['chat_name'])
            await self.channel_layer.group_add(
                self.encoded_chat_name,
                self.channel_name
            )

            await self.channel_layer.group_send(
                self.default_chat, {
                "type" : "SendChatCreation",
                "chat_name": self.chat_name,
                "author": serializer['username'],
                "msg" : msg, 
            })
            return
        if data['type'] == 3: #Chat Removal
            self.chat_name = data['chat_name']
            delete_count, _ = await self.remove_chatroom(self.chat_name, serializer['username'])
            self.encoded_chat_name = await sync_to_async(self.encode)(data['chat_name'])
            
            await self.channel_layer.group_send(
                self.default_chat, {
                "type" : "SendChatDeletion",
                "chat_name": self.chat_name,
                "msg" : 'success' if delete_count > 0 else 'Unknown error', 
            })
            if delete_count > 0: 
                await self.channel_layer.group_discard(self.encoded_chat_name, self.channel_name)
            return
        if data['type'] == 4: #Adding a user to the chat
            self.chat_name = data['chat_name']
            self.encoded_chat_name = await sync_to_async(self.encode)(data['chat_name'])
            await self.channel_layer.group_add(
                self.encoded_chat_name,
                self.channel_name
            )
            return
        self.encoded_chat_name = await sync_to_async(self.encode)(self.chat_name)
        await self.channel_layer.group_send(
            self.encoded_chat_name, {
            "type" : "SendMessage",
            "chat_name": self.chat_name,
            "message" : data['message'], 
            "username" : serializer['username'],
        })
   
    async def SendMessage(self, event):
        await self.save_message(event['chat_name'], event['username'], event['message'])
        await self.send(text_data=json.dumps({
            'data_type': "message",
            'chat_name': event['chat_name'],
            'username': event['username'],
            'message': event['message']
        }))
    
    async def SendChatCreation(self, event):
        print(event['msg'])
        await self.send(text_data=json.dumps({
        'data_type': 'chat_creation',
        'chat_name': event['chat_name'],
        'author': event['author'],
        'msg': event['msg'],
    }))
    
    async def SendChatDeletion(self, event):
         await self.send(text_data=json.dumps({
            'data_type': 'chat_deletion',
            'chat_name': event['chat_name'],
            'msg': event['msg'],
        }))
    
    async def disconnect(self, code):
        if hasattr(self, 'default_chat'):
           await self.channel_layer.group_discard(self.default_chat, self.channel_name)
    
    @database_sync_to_async
    def save_message(self, chat_name, username, message):
        return Message.objects.create(chat_name=chat_name, username=username, message=message)
    
    @database_sync_to_async
    def create_chatroom(self, chat_name, username):
        _, created = Channel.objects.get_or_create(chat_name=chat_name, author=username)
        if not created:
            return 'This chatroom already exists!'
        return 'success'
   
    @database_sync_to_async
    def remove_chatroom(self, chat_name, username):
        obj = Channel.objects.filter(chat_name=chat_name).first()
        msgs = Message.objects.filter(chat_name=chat_name)
        if obj.author == username:
            msgs.delete()
            return obj.delete()
        else:
            async_to_sync(self.close)(code=4001)
    
    @database_sync_to_async
    def get_previous_messages(self):
        return Message.objects.filter()
    
    def encode(self, name):
        encoded = base64.urlsafe_b64encode(name.encode('utf-8')).decode('ascii')
        print(encoded)
        return encoded.rstrip("=")

    def decode(self, encoded_name):
        padding = '=' * (4 - len(encoded_name) % 4)
        encoded_name_with_padding = encoded_name + padding
        return base64.urlsafe_b64decode(encoded_name_with_padding.encode('ascii')).decode('utf-8')