from django.urls import path
from .views import *

urlpatterns = [
    path('', chat, name='chatroom'),
    path('api/chat/<int:id_>/', get_chat_, name="get_chat_api"),
    path('api/user/<int:user_id>/', get_user, name="get_profile_api"),
    path('api/threads/<int:user_id>/', user_chats, name="get_threads_api"),
    path('<chat_id>/message/<id_>/delete/', delete_msg, name="del_4_you"),
    path('<chat_id>/update/secret/', update_chat_secret, name="update_secret")
]
