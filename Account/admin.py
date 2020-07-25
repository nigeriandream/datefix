from django.contrib import admin
from .models import User, Couple, Notification, PersonalityTest

# Register your models here.

admin.site.register(User)
admin.site.register(Couple)
admin.site.register(Notification)
admin.site.register(PersonalityTest)
