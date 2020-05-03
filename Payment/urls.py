from django.urls import path
from .views import *

urlpatterns = [
    path ('pay/', payment, name='payment')
]
