import json
from django.db.models import Q

from Account.models import User, Couple
from datetime import datetime, timedelta
from .models import ChatThread


def select_match(chat_thread, user, you):
    position = chat_thread.position(user)
    if position == 'first':
        chat_thread.date_first = True
        chat_thread.save()

    if position == 'second':
        chat_thread.date_second = True
        chat_thread.save()

    if (position == 'first' and chat_thread.date_second) or (
            position == 'second' and chat_thread.date_first):
        try:
            Couple.objects.get(first_partner_id=you.id, second_partner_id=user.id)
        except Couple.DoesNotExist:
            try:
                Couple.objects.get(first_partner_id=user.id, second_partner_id=you.id)
            except Couple.DoesNotExist:
                couple = Couple.objects.create(first_partner_id=chat_thread.first_user_id,
                                               second_partner_id=chat_thread.second_user_id,
                                               datetime=datetime.now(), couple_name=chat_thread.chat_name())
                for i in [you, user]:
                    couple_list = json.loads(i.couple_ids)
                    if couple.id not in couple_list:
                        couple_list.append(couple.id)
                        i.couple_ids = json.dumps(couple_list)
                        i.save()

        end_session(chat_thread, user, you)
        try:
            couple = Couple.objects.get(first_partner_id=you.id, second_partner_id=user.id)
            return couple.id
        except Couple.DoesNotExist:
            couple = Couple.objects.get(first_partner_id=user.id, second_partner_id=you.id)
            return couple.id
    return f" You have accepted {user.username}. Awaiting Response from {user.username}"


def end_session(chat_thread, user, you):
    list_ = you.matches_()
    try:
        list_.remove(user.id)
        you.matches = json.dumps(list_)
        if you.session == 2:
            you.session = 1
        elif you.session == 1:
            you.session = 0
        you.save()
    except ValueError:
        pass

    list_ = user.matches_()
    try:
        list_.remove(you.id)
        user.matches = json.dumps(list_)
        if user.session == 2:
            user.session = 1
        elif user.session == 1:
            user.session = 0
        user.save()
    except ValueError:
        pass

    email_chat(chat_thread, user)
    email_chat(chat_thread, you)
    chat_thread.delete()
    return


def email_chat(chat_thread, user):
    other_user = chat_thread.get_receiver(user)
    user_chat = chat_thread.get_chat_file(user)
    from django.core.mail import EmailMessage
    message = EmailMessage(f'Chat Text File Between You and {user.username} from Datefix.com',
                           f'Hi {other_user.username},  This message indicates that the chat session between the two of you '
                           f'is formally over. '
                           'Attached to this email address is a .txt file of the chat between the two of you. '
                           ''
                           'Datefix Team.', 'admin@datefix.com', [user.email])
    message.attach_file(f'{user_chat.name}', 'text/plain')
    message.send(True)
    import os
    os.remove(f'{user_chat.name}')


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


def get_chat(chat_id, user):
    chat_thread = ChatThread.objects.get(id=chat_id)
    return json.dumps(chat_thread.get_chat(chat_thread.position(user)))


def get_chat_threads(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        chats = ChatThread.objects.filter(Q(first_user_id=request.user.id) | Q(
            second_user_id=request.user.id)).order_by('-last_message_date')
        data = [{
            "chat_id": x.id,
            "chat_link": ''.join(['/chat/api/chat/', str(x.id)]),
            "username": x.get_receiver(user).username,
            "status": x.get_receiver(user).status,
            "first_name": x.get_receiver(user).first_name,
            "last_name": x.get_receiver(user).last_name,
            "profile_picture": profile_picture(x.get_receiver(user).profile_picture),
            "last_message": last_message(x),
            "expired": x.expired()
        } for x in chats]
        return json.dumps({'user_id': request.user.id, "chat_threads": data})


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
                'time': chat_thread.last_message().datetime.time().strftime('%I:%M %p'),
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
                           'profile_pic': profile_picture(user.profile_picture),
                           'status': user.status,
                           'threads': user.chatThreads()})


def create_chat(request, your_id, user_id):
    if int(request.user.id) == int(user_id):
        return 'You Cannot Chat With Yourself.'
    try:
        ChatThread.objects.get(first_user_id=your_id, second_user_id=user_id)
        return 'This Chat Thread Object Already Exists'
    except ChatThread.DoesNotExist:
        try:
            ChatThread.objects.get(first_user_id=user_id, second_user_id=your_id)
            return 'This Chat Thread Object Already Exists'
        except ChatThread.DoesNotExist:
            from Datefix.algorithms import get_key
            user = User.objects.get(id=your_id)
            if user.session == -1:
                user.session = 1
            elif user.session == 1:
                user.session = 2
            if user_id not in user.matches_():
                list_ = user.matches_()
                list_.append(user_id)
                user.matches = json.dumps(list_)
            user.save()
            user = User.objects.get(id=user_id)
            if user.session == -1:
                user.session = 1
            elif user.session == 1:
                user.session = 2
            if your_id not in user.matches_():
                list_ = user.matches_()
                list_.append(your_id)
                user.matches = json.dumps(list_)
            user.save()
            chat = ChatThread()
            chat.first_user_id = your_id
            chat.second_user_id = user_id
            chat.secret = get_key(f'{request.user.id}{datetime.now().__str__()}{user_id}')
            chat.expiry_date = datetime.now() + timedelta(days=7)
            chat.date_created = datetime.now()
            chat.save()
            return {"status": 200, "message": f'A Chat Thread Object has been created for you and the '
                                              f'user with ID {user_id}',
                    "data": get_chat(chat.id, user=request.user)}


def has_chat(user):
    no_of_chats = user.matches_()
    if len(no_of_chats) > 0:
        print('has chat')
        return True
    print('has no chat')
    return False


def session_ended(user):
    users = User.objects.filter(Q(jilted_matches__contains=f"[{user.id},") |
                                Q(jilted_matches__contains=f',{user.id}]'))
