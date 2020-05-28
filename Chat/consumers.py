import asyncio
import json
from Account.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.utils.datetime_safe import datetime
from .models import Chat_Thread, Chat_Message
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({"type": "websocket.accept"})
        
    
    async def websocket_receive(self, event):
            self.chat_data = json.loads(event['text'])
            if self.chat_data['function'] == 'connect':
                chat_id = self.chat_data['chat_id']
                self.thread_obj = await self.get_thread(chat_id)
                self.me = await self.get_user(self.chat_data['username'])
                self.other_user = await self.get_receiver(self.thread_obj,self.me)
                chat_room = f"chat_{self.thread_obj.id}"
                print("Connected to "+chat_room)
                self.chat_room = chat_room
                await self.channel_layer.group_add(
                    chat_room,
                    self.channel_name
                )
            if self.chat_data['function'] == 'status':
                await self.update_status(int(self.chat_data['message_id']))
                print('updated - delivered')
                await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data})
            elif self.chat_data['function'] == 'message':                                
                self.chat_data['datetime'] = datetime.now()
                self.chat_data['status'] = 'sent'
                await self.save_message(self.thread_obj, self.chat_data)
                del self.chat_data['datetime']
                print(self.chat_data)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {"type": "send_message",
                    "data": self.chat_data}
                )
            elif self.chat_data['function'] == 'isDelivered':
                await self.update_status(int(self.chat_data['message_id']))
                await self.channel_layer.group_send(
                    self.chat_room,
                    {"type": "send_message",
                    "data": self.chat_data}
                )
            elif self.chat_data['function'] in ['isTyping', 'notTyping', 'available']:
                await self.channel_layer.group_send(
                    self.chat_room,
                    {"type": "send_message",
                     "data": self.chat_data}
                )
            
            elif self.chat_data['function'] == 'delete':
                await self.delete_message(int(self.chat_data['message_id']))
                await self.channel_layer.group_send(
                    self.chat_room,
                    {"type": "send_message", "data": self.chat_data}
                )

            
    
    async def send_message(self, event):
        await self.send({"type":"websocket.send", "text": json.dumps(event['data'])})       
    async def websocket_disconnect(self, event):
        print("disconnected", event)
        
    @database_sync_to_async   
    def get_thread(self, id_):
        return Chat_Thread.objects.get(id=id_)
    
    @database_sync_to_async 
    def get_receiver(self,chat, user):
        return chat.get_receiver(user)
    
    @database_sync_to_async   
    def save_message(self,chat,data):
        encrypted_data = chat.encrypt(data['message'])
        chat_msg = Chat_Message.objects.create(sender_id=int(data['sender_id']),chat=chat,
                                          text=encrypted_data,datetime=data['datetime'],
                                            send_status=data['status'])
        self.chat_data['message_id'] = chat_msg.id
        return chat_msg
    
    @database_sync_to_async                                      
    def get_user(self,username):
        return User.objects.get(username=username)
    
    
    @database_sync_to_async         
    def update_status(self, id_):
        msg = Chat_Message.objects.get(id=id_)
        msg.send_status = 'delivered'
        msg.save()
        self.chat_data['status'] = 'delivered'
        return msg
    
    @database_sync_to_async  
    def delete_message(self, id_):
        msg = Chat_Message.objects.get(id=id_)
        if msg.expired() is False:
            msg.delete()
            self.chat_data['result'] = 'Deleted'
            return 'Deleted'
        self.chat_data['result'] = 'Not Deleted'
        return 'Not Deleted'
        
        