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


def chat(request, thread_id):
    user = User.objects.get(id=request.user.id)
    chat = Chat_Thread.objects.get(id=thread_id)
    chat.self_delete()
    chat.show_detail()
    # if request.method == 'GET' and user.payed is True and (chat.first_user == user or chat.second_user == user):
    if request.method == 'GET' and (chat.first_user == user or chat.second_user == user):
        return render(request, 'Chat/chat.html', {'messages': chat.chat_messages(chat.position(user)),
                                                  'show': chat.show_details, 'receiver': chat.get_receiver(user),
                                                  'chat_id': chat.id})
    elif request.method == 'POST':
        return redirect('chatroom', chat.id)
    else:
        return redirect('dashboard')


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
