from django.shortcuts import render, redirect, HttpResponse
from .algorithms import create_private_key, get_chat, get_profile, get_chat_threads, delete_message

from Account.models import User


# Create your views here.


def chat(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if len(user.matches()) == 2:
            return render(request, 'Chat/chat.html')
        return redirect('dashboard')


def get_chat_(request, id_):
    return HttpResponse(get_chat(request, id_))


def get_user(request, user_id):
    return HttpResponse(get_profile(request, user_id))


def user_chats(request, user_id):
    return HttpResponse(get_chat_threads(request, user_id))


def delete_msg(request, chat_id, id_):
    return HttpResponse(delete_message(request, chat_id, id_))
