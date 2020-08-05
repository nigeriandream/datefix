import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from Datefix import settings
import json
from django.db.models import Q

# Create your models here.
from Datefix.algorithms import get_key


class User(AbstractUser):
    sex = models.CharField(max_length=6, default=None, null=True)
    phone = models.CharField(max_length=16, default=None, null=True)
    user_data = models.TextField(default='{}')
    choice_data = models.TextField(default='{}')
    deal_breaker = models.CharField(max_length=64, default='[]')
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    matches = models.CharField(max_length=10, default='[]')
    successful_matches = models.TextField(default='{}')
    no_matches = models.TextField(default='[]')
    jilted_matches = models.TextField(default='[]')
    notification = models.TextField(default='[]')
    profile_changed = models.BooleanField(default=False)
    couple_ids = models.CharField(max_length=16, default='[]')
    payed = models.BooleanField(default=False)
    session = models.IntegerField(default=-1)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=64, default='Offline')

    def successful_list(self):
        if self.successful_matches is None or self.successful_matches == '':
            return []
        return json.loads(self.successful_matches)

    def no_list(self):
        if self.no_matches == '' or self.no_matches is None:
            return []
        return json.loads(self.no_matches)

    def jilted_list(self):
        if self.jilted_matches == '' or self.jilted_matches is None:
            return []
        return self.jilted_matches.split(',')

    def matches_(self):
        if self.matches is None or self.matches == '':
            return []
        return json.loads(self.matches)

    def complete_match(self):
        if self.matches_().__len__() < 2:
            return False
        return True

    def is_couple(self):
        try:
            Couple.objects.get(first_partner=self)
            return True
        except Couple.DoesNotExist:
            try:
                Couple.objects.get(second_partner=self)
                return True
            except Couple.DoesNotExist:
                return False

    def user_data_(self):
        if self.user_data is None or self.user_data == '':
            return {}
        return json.loads(self.user_data)

    def choice_data_(self):
        if self.choice_data is None or self.choice_data == '':
            return {}
        return json.loads(self.choice_data)

    def notifications(self):
        notifications = Notification.objects.filter(Q(receiver=self.id) | Q(general=True)).order_by('-datetime')
        if self.notification is None or self.notification == '':
            return notifications
        notify = json.loads(self.notification)
        return [x for x in notifications if str(x.id) not in notify['deleted']]

    def new_notifications(self):
        notifications = Notification.objects.filter(Q(receiver=self.id) | Q(general=True)).order_by('-datetime')
        if self.notification is None or self.notification == '':
            return notifications.count()
        notify = json.loads(self.notification)
        return [x for x in notifications if
                (str(x.id) not in notify['read']) and (str(x.id) not in notify['deleted'])].__len__()

    def couple_list(self):
        return json.loads(self.couple_ids)

    def origin(self):
        return self.user_data_()['origin-state']

    def residence(self):
        return self.user_data_()['residence-state']

    def religion(self):
        return self.user_data_()['religion']

    def denomination(self):
        return self.user_data_()['denomination']

    def has_children(self):
        return self.user_data_()['children']

    def personality(self):
        try:
            test_ = PersonalityTest.objects.get(email=self.email)
            return test_.titles()
        except PersonalityTest.DoesNotExist:
            return []

    def chatThreads(self):
        from Chat.models import ChatThread
        threads = ChatThread.objects.filter(Q(first_user_id=self.id) | Q(second_user_id=self.id))
        return list(set([x.id for x in threads]))


class Couple(models.Model):
    first_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='match1')
    second_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='match2')
    couple_name = models.CharField(max_length=30, default='')
    datetime = models.DateTimeField()

    def true_details(self, user_id):
        user = None
        if self.first_partner_id == user_id:
            user = User.objects.get(id=self.second_partner_id)
        if self.second_partner_id == user_id:
            user = User.objects.get(id=self.first_partner_id)
        if user is None:
            return None
        else:
            user_data = json.loads(user.user_data)
            try:
                data = {"firstName": user.first_name,
                        "lastName": user.last_name, "phone": user.phone, "email": user.email,
                        "residential_address": f"{user_data['residence-lga']}, {user_data['residence-state']}",
                        "origin_address": f"{user_data['origin-lga']}, {user_data['origin-state']}"}
            except KeyError:
                data = {"firstName": user.first_name,
                        "lastName": user.last_name, "phone": user.phone, "email": user.email}

            return data


class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    datetime = models.DateTimeField()
    general = models.BooleanField(default=True)
    receiver = models.IntegerField(default=None, null=True)


class PersonalityTest(models.Model):
    email = models.EmailField()
    extraversion = models.TextField(default='{}')
    neurotism = models.TextField(default='{}')
    agreeableness = models.TextField(default='{}')
    conscientiousness = models.TextField(default='{}')
    openness = models.TextField(default='{}')

    def titles(self):
        return [json.loads(self.extraversion)['title'], json.loads(self.neurotism)['title'],
                json.loads(self.agreeableness)['title'], json.loads(self.conscientiousness)['title'],
                json.loads(self.openness)['title']]
