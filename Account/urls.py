from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('match/', matching, name='match'),
    path('results/', results, name='results'),
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
    path('notifications/read/', read_notifications, name='read_notifications'),
    path('notification/<int:id_>/delete/',
         delete_notifications, name='delete_notifications'),
    path('get_data/<type_>/', get_data, name="get_data"),
    path('adjust_minimum/', adjust_min, name="adjust_minimum")
]
