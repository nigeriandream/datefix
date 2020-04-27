from django.urls import path
from .views import *

urlpatterns = [
    path('<int:thread_id>/', chat, name='chatroom'),
    path('all/', all_chats, name='all_chats'),
    path('match_<int:match_id>/choice/', request_, name="match_choice"),
    path('api/chat/<int:id_>/', get_chat, name="get_chat_api"),
    path('<chat_id>/message/<id_>/delete/', delete_message, name="del_4_you")
]
