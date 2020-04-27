from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('data_details/', data_details, name='data_details'),
    path('update_profile/', update_profile, name='update_profile'),
    path('match/', matching, name="match"),
    path('notifications/read/', read_notifications, name='read_notifications'),
    path('notification/<int:id_>/delete/', delete_notifications, name='delete_notifications' )
]
