from django.shortcuts import render, redirect, HttpResponse


# Create your views here.


def chat(request):
    if request.user.is_authenticated:
        from Account.models import User
        user = User.objects.get(id=request.user.id)
        from Chat.algorithms import has_chat
        if has_chat(user):
            return render(request, 'Chat/chat.html')
        return redirect('dashboard')
    return redirect('home')


def get_chat_(request, id_):
    if request.method == 'GET':
        from Chat.algorithms import get_chat
        return HttpResponse(get_chat(id_, request.user))


def get_user(request, user_id):
    from Chat.algorithms import get_profile
    return HttpResponse(get_profile(request, user_id))


def user_chats(request):
    from Chat.algorithms import get_chat_threads
    return HttpResponse(get_chat_threads(request))


def delete_msg(request, chat_id, id_):
    from Chat.algorithms import delete_message
    return HttpResponse(delete_message(request, chat_id, id_))


def create_chat_api(request, user_id):
    from Chat.algorithms import create_chat
    return HttpResponse(create_chat(request, request.user.id, user_id))
