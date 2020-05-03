from django.contrib import admin
from .models import Chat_Message, Chat_Thread

admin.site.register(Chat_Message)
admin.site.register(Chat_Thread)

# Register your models here.
