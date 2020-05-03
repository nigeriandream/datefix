from Account.models import User
from datetime import datetime
from Account.algorithms import get_new_match
from .models import Chat_Thread, Chat_Message
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.PublicKey import RSA 
from binascii import hexlify 
import secrets


def create_private_key():
    secret = secrets.token_hex(32)
    try:
        Chat_Thread.objects.get(secret=secret)
        create_private_key()
    except Chat_Thread.DoesNotExist:
        secret_file = '.'.join([secret, 'pem'])
        private_key = RSA.generate(1024).export_key().decode()
        with open(secret_file, 'w') as pr:
            pr.write(private_key)
        return secret
    
    
    


def create_chat(user, match):
    try:
        Chat_Thread.objects.get(first_user=user, second_user=match)
    except Chat_Thread.DoesNotExist:
        try:
            Chat_Thread.objects.get(first_user=match, second_user=user)
        except Chat_Thread.DoesNotExist:
            peep = User.objects.get(id=match.id)
            chat = Chat_Thread()
            chat.first_user = user
            chat.second_user = peep
            chat.datetime = datetime.now()
            chat.secret = create_private_key()
            chat.save()
            
    
def delete_chat(user, match):
    try:
        Chat_Thread.objects.get(first_user=user, second_user=match).delete()
    except Chat_Thread.DoesNotExist:
        try:
            Chat_Thread.objects.get(first_user=match, second_user=user).delete()
        except Chat_Thread.DoesNotExist:
            pass
    
def reply_request(choice, user, match):
    if choice is True:
        create_chat(user, match)
        send_message(user, match)
        return True
        
    else:
        delete_chat(user, match)
        if get_new_match(user, match) is True:
            return None
        else:
            return False
      
 
def send_message(user, match):
     pass
     
    

def delete_msg(user, msg_id, chat, type_):
    if type_ == 'me':
        if chat.position(user) == 'first':
            chat.first_deleted = ','.join(chat.first_deleted_().append(str(msg_id)))
        else:
            chat.second_deleted = ','.join(chat.second_deleted_().append(str(msg_id)))
    elif type_ == 'everyone':
        Chat_Message.objects.get(id=msg_id).delete()
    chat.save()
    
    

def in_my_chat(user, match):
    try:
        Chat_Thread.objects.get(first_user=user, second_user=match)
        return True
    except Chat_Thread.DoesNotExist:
        try:
            Chat_Thread.objects.get(first_user=match, second_user=user)
            return True
        except Chat_Thread.DoesNotExist:
            return False