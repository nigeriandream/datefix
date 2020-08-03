from django.urls import path

from Account.views import encrypt, decrypt
from .views import *

urlpatterns = [
    path('', chat, name='chatroom'),
    path('end_session/', session_end, name="end_session"),
    path('api/chat/<int:id_>/', get_chat_, name="get_chat_api"),
    path('api/user/<int:user_id>/', get_user, name="get_profile_api"),
    path('api/threads/', user_chats, name="get_threads_api"),
    path('api/encrypt/', encrypt, name="encrypt_msg"),
    path('api/decrypt/', decrypt, name="decrypt_msg"),
    path('api/create/<user_id>/', create_chat_api, name="create_chat"),
    path('<chat_id>/message/<id_>/delete/', delete_msg, name="del_4_you"),
    path('api/test/jilt/<int:chat_id>/', test_jilt, name="jilt"),
    path('api/test/accept/<int:chat_id>/', test_accept, name="accept")

]
