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
