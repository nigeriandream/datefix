from django.contrib import admin
from .models import ChatMessage, ChatThread

admin.site.register(ChatMessage)
admin.site.register(ChatThread)

# Register your models here.
