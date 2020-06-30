import json

from django.db.models import Q

from Account.models import User, Couple
from datetime import datetime
from .models import ChatThread, ChatMessage
from Crypto.PublicKey import RSA
import secrets


def create_private_key():
    secret = secrets.token_hex(32)
    try:
        ChatThread.objects.get(secret=secret)
        create_private_key()
    except ChatThread.DoesNotExist:
        secret_file = f'Secret/{secret}.pem'
        private_key = RSA.generate(1024).export_key().decode()
        with open(secret_file, 'w') as pr:
            pr.write(private_key)
        return secret


def create_chat(user, match):
    try:
        ChatThread.objects.get(first_user_id=user.id, second_user_id=match.id)
    except ChatThread.DoesNotExist:
        try:
            ChatThread.objects.get(first_user_id=match.id, second_user_id=user.id)
        except ChatThread.DoesNotExist:
            chat = ChatThread()
            chat.first_user = user
            chat.second_user = match
            chat.datetime = datetime.now()
            chat.secret = create_private_key()
            chat.save()


def select_match(chat_thread, user, you):
    if chat_thread.position(user) == 'first':
        chat_thread.date_first = True

    if chat_thread.position(user) == 'second':
        chat_thread.date_second = True

    if (chat_thread.position(user) == 'first' and chat_thread.date_second) or (
            chat_thread.position(user) == 'second' and chat_thread.date_first):
        try:
            Couple.objects.get(couple_name=chat_thread.chat_name())
        except Couple.DoesNotExist:
            Couple.objects.create(first_partner_id=chat_thread.first_user.id,
                                  second_partner_id=chat_thread.second_user.id,
                                  datetime=datetime.now(), couple_name=chat_thread.chat_name())
        end_session(chat_thread, user, you)
    return


def end_session(chat_thread, user, you):
    list_ = you.matches_()
    list_.remove(user.id)
    you.matches = json.dumps(list_)
    you.save()
    list_ = user.matches_()
    list_.remove(you.id)
    user.matches = json.dumps(list_)
    user.save()
    chat_thread.delete()
    return


def reject(you, user):
    if user.id not in json.loads(you.jilted_matches):
        list_ = json.loads(you.jilted_matches)
        list_.append(user.id)
        you.jilted_matches = json.dumps(list_)
        you.save()
    return


def jilt(chat, you, user):
    reject(you, user)
    reject(user, you)
    end_session(chat, user, you)
    return


def get_chat(request, id_):
    if request.method == 'GET':
        chat_thread = ChatThread.objects.get(id=id_)
        return json.dumps(chat_thread.get_chat(chat_thread.position(request.user)))


def get_chat_threads(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        chats = ChatThread.objects.filter(Q(first_user_id=request.user.id) | Q(
            second_user_id=request.user.id)).order_by('last_message_date')
        data = [{
            "chat_id": x.id,
            "chat_link": ''.join(['/chat/api/chat/', str(x.id)]),
            "username": x.get_receiver(user).username,
            "first_name": x.get_receiver(user).first_name,
            "last_name": x.get_receiver(user).last_name,
            "profile_picture": profile_picture(x.get_receiver(user).profile_picture),
            "last_message": last_message(x)
        } for x in chats]
        return json.dumps({'user_id': user_id, "chat_threads": data})


def delete_message(request, chat_id, id_):
    chat = ChatThread.objects.get(id=chat_id)
    position = chat.position(request.user)
    list_ = {'first': chat.first_deleted_(), 'second': chat.second_deleted_()}
    list_ = list_[position]
    list_.append(str(id_))
    if position == 'first':
        chat.first_deleted = ','.join(list_)
    elif position == 'second':
        chat.second_deleted = ','.join(list_)
    return id_


def profile_picture(image):
    try:
        return image.url
    except ValueError:
        return None


def last_message(chat_thread):
    if chat_thread.last_message() is not None:
        return {'id': chat_thread.last_message().id,
                'time': chat_thread.last_message().datetime.time().__str__(),
                'message': chat_thread.last_message_text(),
                'sender_id': chat_thread.last_message().sender.id,
                'sender': chat_thread.last_message().sender.username,
                'status': chat_thread.last_message().send_status}
    else:
        return None


def get_profile(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        return json.dumps({'username': user.username,
                           'first_name': user.first_name, 'last_name': user.last_name,
                           'profile_pic': profile_picture(user.profile_picture)})
