import asyncio
import json
from Account.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.utils.datetime_safe import datetime
from .models import ChatThread, ChatMessage


async def login(self):
    self.chat_data['status'] = 'Online'
    await self.channel_layer.group_send(
        self.general,
        {"type": "send_message",
         "data": self.chat_data})


async def logout(self):
    self.set_user_status('Offline')
    self.chat_data['status'] = self.me.status
    await self.channel_layer.group_send(
        self.general,
        {"type": "send_message",
         "data": self.chat_data})


class ChatConsumer(AsyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.chat_data = {}
        self.thread_obj = None
        self.me = None
        self.general = 'DateFix'
        self.other_user = None
        self.chat_room = ''

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({"type": "websocket.accept"})
        await self.channel_layer.group_add(
            self.general,
            self.channel_name
        )

    async def websocket_receive(self, event):
        self.chat_data = json.loads(event['text'])

        if self.chat_data['function'] == 'login':
            await login(self)

        if self.chat_data['function'] == 'connect':
            try:
                chat_id = self.chat_data['chat_id']
                self.thread_obj = await self.get_thread(chat_id)
                self.me = await self.get_user(self.chat_data['username'])
                self.other_user = await self.get_receiver(self.thread_obj, self.me)
                chat_room = f"chat_{self.thread_obj.id}"
                print("Connected to " + chat_room)
                self.chat_room = chat_room
                await self.channel_layer.group_add(
                    chat_room,
                    self.channel_name
                )

                await self.set_user_status('Online')
            except (ChatThread.DoesNotExist, AttributeError):
                pass

            self.chat_data['chat_room'] = self.chat_room
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data})
            await self.channel_layer.group_send(
                self.general,
                {"type": "send_message",
                 "data": {"username": self.chat_data['username'], "status": "Online"}})

        if self.chat_data['function'] == 'disconnect':
            await self.set_user_status('Offline')
            await self.channel_layer.group_send(
                self.general,
                {"type": "send_message",
                 "data": self.chat_data})
        if self.chat_data['function'] == 'status':
            await self.update_status(int(self.chat_data['message_id']))
            print('updated - delivered')
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data})
        if self.chat_data['function'] == 'message':
            self.chat_data['datetime'] = datetime.now()
            self.chat_data['time'] = self.chat_data['datetime'].time().strftime('%I:%M %p')
            self.chat_data['date'] = self.chat_data['datetime'].date().strftime('%e - %b - %Y')
            self.chat_data['status'] = 'sent'
            await self.save_message(self.thread_obj, self.chat_data)
            del self.chat_data['datetime']
            print(self.chat_data)
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data}
            )
        if self.chat_data['function'] == 'isDelivered':
            await self.update_status(int(self.chat_data['message_id']))
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data}
            )
        if self.chat_data['function'] in ['isTyping', 'notTyping', 'available']:
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message",
                 "data": self.chat_data}
            )
        if self.chat_data['function'] == 'delete':
            await self.delete_message(int(self.chat_data['message_id']))
            await self.channel_layer.group_send(
                self.chat_room,
                {"type": "send_message", "data": self.chat_data}
            )
        if self.chat_data['function'] == 'jilt':
            await self.reject()
            await self.channel_layer.group_send(
                self.general,
                {"type": "send_message",
                 "data": self.chat_data})
        if self.chat_data['function'] == 'accept':
            if 'username' in self.chat_data and 'chat_id' in self.chat_data:
                await self.get_thread(self.chat_data['chat_id'])
                await self.get_user(self.chat_data['username'])
                await self.get_receiver(self.thread_obj, self.me)

            await self.choose()
            self.chat_data['chat_id'] = self.thread_obj.id
            await self.channel_layer.group_send(
                self.general,
                {"type": "send_message",
                 "data": self.chat_data})

        if self.chat_data['function'] == 'logout':
            await logout(self)
            from django.shortcuts import redirect
            return redirect('logout')

    async def send_message(self, event):
        await self.send({"type": "websocket.send", "text": json.dumps(event['data'])})

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        # tell chat mate you're offline

    @database_sync_to_async
    def get_thread(self, id_):
        self.thread_obj = ChatThread.objects.get(id=id_)
        return self.thread_obj

    @database_sync_to_async
    def get_receiver(self, chat, user):
        self.other_user = chat.get_receiver(user)
        return self.other_user

    @database_sync_to_async
    def save_message(self, chat, data):
        from Chat.algorithms import activate_expiration
        activate_expiration(chat=chat, user=self.me)
        encrypted_data = chat.encrypt(data['message'])
        chat_msg = ChatMessage.objects.create(sender_id=int(data['sender_id']), chat=chat,
                                              text=encrypted_data, datetime=data['datetime'],
                                              send_status=data['status'])
        self.thread_obj.last_message_date = chat_msg.datetime
        self.thread_obj.save()
        self.chat_data['message_id'] = chat_msg.id
        return chat_msg

    @database_sync_to_async
    def get_user(self, username):
        self.me = User.objects.get(username=username)
        return self.me

    @database_sync_to_async
    def update_status(self, id_):
        msg = ChatMessage.objects.get(id=id_)
        msg.send_status = 'delivered'
        msg.save()
        self.chat_data['status'] = 'delivered'
        return msg

    @database_sync_to_async
    def choose(self):
        from Chat.algorithms import select_match
        try:
            data = select_match(self.thread_obj, self.other_user, self.me)
            try:
                int(data)
                self.chat_data['result'] = {'status': 'successful', 'couple_id': data}
            except ValueError:
                self.chat_data['result'] = {'status': 'successful', 'response': data}
        except ChatThread.DoesNotExist:
            pass

    @database_sync_to_async
    def reject(self):
        from Chat.algorithms import jilt
        jilt(self.thread_obj, self.other_user, self.me)
        self.chat_data['result'] = 'succeed'
        return

    @database_sync_to_async
    def delete_message(self, id_):
        msg = ChatMessage.objects.get(id=id_)
        if msg.expired() is False:
            msg.delete()
            self.chat_data['result'] = 'Deleted'
            return 'Deleted'
        self.chat_data['result'] = 'Not Deleted'
        return 'Not Deleted'

    @database_sync_to_async
    def set_user_status(self, status):
        user = self.me
        if status == 'Online' and (user.status == 'Offline' or 'Last seen' in user.status):
            user.status = 'Online'
            user.save()

        if status == 'Offline' and user.status == 'Online':
            user.status = f"Last seen at {datetime.now().time().strftime('%I:%M %p')} " \
                          f"on {datetime.now().date().strftime('%e - %b - %Y')}."
            user.save()

        self.chat_data['status'] = user.status
        return
