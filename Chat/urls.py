from django.urls import path

from Account.views import encrypt, decrypt
from .views import *

urlpatterns = [
    path('', chat, name='chatroom'),
    path('api/chat/<int:id_>/', get_chat_, name="get_chat_api"),
    path('api/user/<int:user_id>/', get_user, name="get_profile_api"),
    path('api/threads/<int:user_id>/', user_chats, name="get_threads_api"),
    path('api/encrypt/', encrypt, name="encrypt_msg"),
    path('api/decrypt/', decrypt, name="decrypt_msg"),
    path('api/create/<user_id>/', create_chat_api, name="create_chat"),
    path('<chat_id>/message/<id_>/delete/', delete_msg, name="del_4_you"),

]
