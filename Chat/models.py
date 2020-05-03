from django.db import models
from Account.models import User
from django.conf import settings
from datetime import timedelta,timezone
from django.utils.datetime_safe import datetime
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.PublicKey import RSA 


# Create your models here.

class Chat_Thread(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='chatter1')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.DO_NOTHING, related_name='chatter2')
    show_first = models.BooleanField(default=True)
    show_second = models.BooleanField(default=True)
    date_created = models.DateTimeField()
    date_first = models.NullBooleanField(default=None, blank=True, null=True)
    date_second = models.NullBooleanField(default=None, blank=True, null=True)
    show_details = models.BooleanField(default=False)
    first_deleted = models.TextField()
    second_deleted = models.TextField()
    secret = models.CharField(max_length=64)
    last_message_date = models.DateTimeField(default=None, null=True)
    
    
    
    def self_delete(self):
        if (not self.show_first and not self.show_second):
            self.delete()
        
        if (self.date_first is False or self.date_second is False):
            self.delete()
        
    
    def show_detail(self):
        if self.date_created == (self.date_created + (timedelta(days=7))):
            self.show_details = True
    
    def first_deleted_(self):
        return str(self.first_deleted).split(',')
    
    def second_deleted_(self):
        return str(self.second_deleted).split(',')
    
    def chat_messages(self, user_position):
        list_ = {'first': self.first_deleted_(), 'second': self.second_deleted_()}
        chat_message_items = [x for x in Chat_Message.objects.all().filter(chat_id=self.id).order_by('datetime') \
                if x.id not in list_[user_position]]
        decrypted_messages = [self.decrypt(x.text) for x in chat_message_items]
        return zip(chat_message_items, decrypted_messages)
    
    def get_chat(self, user_position):
        list_ = {'first': self.first_deleted_(), 'second': self.second_deleted_()}
        chat_message_items = [x for x in Chat_Message.objects.all().filter(chat_id=self.id).order_by('datetime') \
                if x.id not in list_[user_position]]
        data = []
        for i in chat_message_items:
            data.append({'id': i.id, 
                          'time': i.datetime.time().__str__(),
                          'message': self.decrypt(i.text),
                          'sender_id': i.sender.id,
                           'sender': i.sender.username,
                           'status': i.send_status})
        data = {'chat_list': data}
        return data
    
    def get_receiver(self, user):
        if self.first_user.id == user.id:
            return self.second_user
        else:
            return self.first_user
    
    def position(self, user):
        if self.first_user.id == user.id:
            return 'first'
        return 'second'
    
    def last_message(self):
        msg = Chat_Message.objects.filter(chat=self).order_by('-datetime')
        if msg.count() == 0:
            return None
        return msg[0]
    
    def last_message_text(self):
        return self.decrypt(self.last_message().text)
    
    def encrypt(self, data):
        pr= RSA.import_key(open('.'.join([self.secret, 'pem']), 'r').read())
        cipher_text = PKCS1_OAEP.new(key=pr.publickey()).encrypt(data.encode())
        return cipher_text


    def decrypt(self, cipher_text):
        pr= RSA.import_key(open('.'.join([str(self.secret), 'pem']), 'r').read())
        decrypt = PKCS1_OAEP.new(key=pr)
        return decrypt.decrypt(cipher_text).decode()
    

    def no_unread_msg(self, user):
        receiver = self.get_receiver(user)
        position = self.position(user)
        list_ = {'first': self.first_deleted_(), 'second': self.second_deleted_()}
        chat_message_items = [x for x in Chat_Message.objects.filter(chat=self)\
                              .filter(sender=receiver).filter(send_status='sent').order_by('datetime') \
                if x.id not in list_[position]]
        return chat_message_items.__len__()
        
    def first_msg_today(self):
        chat_msg = Chat_Message.objects.filter(chat=self).filter(datetime=datetime.today()).order_by('id')
        return chat_msg[0]
    
class Chat_Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.DO_NOTHING)
    text = models.BinaryField()
    datetime = models.DateTimeField()
    send_status = models.CharField(max_length=20, choices=(('sent', 'sent'), ('delivered', 'delivered')))
    chat = models.ForeignKey(Chat_Thread, on_delete=models.CASCADE)
    
    def expired(self):
        if (datetime.now(timezone.utc) - self.datetime) > timedelta(seconds=180):
            return True
        return False
    
    