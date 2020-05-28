from django.shortcuts import render, redirect, HttpResponse
from .algorithms import reply_request, create_private_key
from .models import Chat_Message, Chat_Thread
from Account.models import User
from django.utils.datetime_safe import datetime
from django.db.models import Q
import json

# Create your views here.


def all_chats(request):
    # user = User.objects.get(id=request.user.id)
    # if request.method == 'GET' and user.payed is True:
    #     chats = Chat_Thread.objects.filter(Q(first_user_id=request.user.id)|Q(second_user_id=request.user.id)).order_by('last_message_date')
    #     unread_msg = [x.no_unread_msg(user) for x in chats]
    #     data = zip(chats, unread_msg)
    #     print(unread_msg[0])
    #     return render(request, 'Chat/all_chat.html', {'data': data})
    # else:
    return redirect('dashboard')


def chat(request):
    return render(request, 'Chat/chat.html')

def request_(request, match_id):
    user = User.objects.get(id=request.user.id)
    match = User.objects.get(id=match_id)
    if request.method == 'POST':
        if request.POST['accept']:
            reply = reply_request(True, user, match)
            return redirect('all_chats')
        elif request.POST['decline']:
            reply = reply_request(False, user, match)
            if reply is None:
                return redirect('dashboard')
            elif reply is False:
                request.session['change min'] = True
                return redirect('data_details')


def get_chat(request, id_):
    if request.method == 'GET':
        chat = Chat_Thread.objects.get(id=id_)
        return HttpResponse(json.dumps(chat.get_chat(chat.position(request.user))))


def get_profile(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        return HttpResponse(json.dumps({'username': user.username,
                                        'first_name': user.first_name, 'last_name': user.last_name, 'profile_pic': profile_picture(user.profile_picture)}))


def get_chat_threads(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        chats = Chat_Thread.objects.filter(Q(first_user_id=request.user.id) | Q(
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
        return HttpResponse(json.dumps({'user_id': user_id, "chat_threads": data}))


def profile_picture(image):
    try:
        return image.url
    except ValueError:
        return None


def last_message(chat):
    if chat.last_message() is not None:
        return {'id': chat.last_message().id,
                'time': chat.last_message().datetime.time().__str__(),
                'message': chat.last_message_text(),
                'sender_id': chat.last_message().sender.id,
                'sender': chat.last_message().sender.username,
                'status': chat.last_message().send_status}
    else:
        return None


def delete_message(request, chat_id, id_):
    chat = Chat_Thread.objects.get(id=chat_id)
    position = chat.position(request.user)
    list_ = {'first': chat.first_deleted_(), 'second': chat.second_deleted_()}
    list_ = list_[position]
    list_.append(str(id_))
    if position == 'first':
        chat.first_deleted = ','.join(list_)
    elif position == 'second':
        chat.second_deleted = ','.join(list_)
    return HttpResponse(id_)


def create_key(request):
    key = create_private_key()
    return HttpResponse(key)
