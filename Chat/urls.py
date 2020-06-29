from django.urls import path
from .views import *

urlpatterns = [
    path('', chat, name='chatroom'),
    path('all/', all_chats, name='all_chats'),
    path('match_<int:match_id>/choice/', request_, name="match_choice"),
    path('api/chat/<int:id_>/', get_chat_, name="get_chat_api"),
    path('api/user/<int:user_id>/', get_user, name="get_profile_api"),
    path('api/threads/<int:user_id>/', user_chats, name="get_threads_api"),
    path('<chat_id>/message/<id_>/delete/', delete_msg, name="del_4_you"),
    path('create/key', create_key, name="create_key")
]
