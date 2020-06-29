from django.shortcuts import render, redirect, HttpResponse
from .algorithms import reply_request, create_private_key, get_chat, get_profile, get_chat_threads, delete_message

from Account.models import User


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


def create_key(request):
    key = create_private_key()
    return HttpResponse(key)


def get_chat_(request, id_):
    return HttpResponse(get_chat(request, id_))


def get_user(request, user_id):
    return HttpResponse(get_profile(request, user_id))


def user_chats(request, user_id):
    return HttpResponse(get_chat_threads(request, user_id))


def delete_msg(request, chat_id, id_):
    return HttpResponse(delete_message(request, chat_id, id_))


