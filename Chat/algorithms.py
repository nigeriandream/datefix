import json

from Account.models import User, Couple
from datetime import datetime
from Account.algorithms import get_new_match
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
        ChatThread.objects.get(first_user=user, second_user=match)
    except ChatThread.DoesNotExist:
        try:
            ChatThread.objects.get(first_user=match, second_user=user)
        except ChatThread.DoesNotExist:
            peep = User.objects.get(id=match.id)
            chat = ChatThread()
            chat.first_user = user
            chat.second_user = peep
            chat.datetime = datetime.now()
            chat.secret = create_private_key()
            chat.save()


def delete_chat(user, match):
    try:
        ChatThread.objects.get(first_user=user, second_user=match).delete()
    except ChatThread.DoesNotExist:
        try:
            ChatThread.objects.get(first_user=match, second_user=user).delete()
        except ChatThread.DoesNotExist:
            pass


def reply_request(choice, user, match):
    if choice is True:
        create_chat(user, match)
        send_message(user, match)
        return True

    else:
        delete_chat(user, match)
        if get_new_match(user, match) is True:
            return None
        else:
            return False


def send_message(user, match):
    pass


def delete_msg(user, msg_id, chat, type_):
    if type_ == 'me':
        if chat.position(user) == 'first':
            chat.first_deleted = ','.join(chat.first_deleted_().append(str(msg_id)))
        else:
            chat.second_deleted = ','.join(chat.second_deleted_().append(str(msg_id)))
    elif type_ == 'everyone':
        ChatMessage.objects.get(id=msg_id).delete()
    chat.save()


def in_my_chat(user, match):
    try:
        ChatThread.objects.get(first_user=user, second_user=match)
        return True
    except ChatThread.DoesNotExist:
        try:
            ChatThread.objects.get(first_user=match, second_user=user)
            return True
        except ChatThread.DoesNotExist:
            return False


def select_match(user, id_):
    chat_thread = ChatThread.objects.get(id=id_)
    if chat_thread.position(user) == 'first':
        chat_thread.date_first = True
    if chat_thread.position(user) == 'second':
        chat_thread.date_second = True
    return


def end_session(id_):
    chat_thread = ChatThread.objects.get(id=id_)
    if chat_thread.date_first is True and chat_thread.date_second is True:
        # send mail to both partners
        Couple.objects.create(first_partner_id=chat_thread.first_user.id,
                              second_partner_id=chat_thread.second_user.id,
                              datetime=datetime.now())
    f = User.objects.get(id=chat_thread.first_user_id)
    s = User.objects.get(id=chat_thread.second_user_id)
    jilt(f, s)
    jilt(s, f)
    chat_thread.delete()
    f.matches = "[]"
    s.matches = "[]"
    f.save()
    s.save()
    return


def jilt(you, user):
    you.jilted_matches = json.loads(user.jilted_matches).append(user.id)
    you.save()
    return
