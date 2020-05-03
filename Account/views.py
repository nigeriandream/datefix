from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from .models import User 
import json
from .algorithms import get_username, match_user
from Chat.algorithms import in_my_chat
# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = auth.authenticate(request, username=email, password=password)
            if user is None:
                return redirect('signup')
            else:
                auth.login(request, user)
                return redirect('dashboard')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'Account/login.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2'] :
            user = User.objects.create_user(
                username= get_username(),
                email = request.POST['email'],
                password = request.POST['password1'],
                first_name = request.POST['first-name'],
                last_name = request.POST['last-name'],
                sex= request.POST['sex'],
                phone = request.POST['phone']    
            )
            user.save()
            return redirect('login')
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, 'Account/signup.html')


def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_details = user.user_data_()
            choice_details = user.choice_data_()
            matches = [User.objects.get(id=int(x)) for x in user.matches_()]
            accepted = [i.id for i in matches if in_my_chat(user, i) is True]
            notifications = user.notifications()
            return render(request, 'Account/profile.html', {'user': user, 'user_details': user_details,
                                                              'choice_details': choice_details,
                                                              'matches': matches,
                                                              'notifications': notifications,
                                                              'new_notification': user.new_notifications(),
                                                              'accepted': accepted})
        else:
            return redirect('login')

    
def matching(request):
    if request.method == 'GET':
        user = User.objects.get(id=GET['user_id'])
        if user.sex == 'female':
            if match_user(user) is True:
                return HttpResponse(json.dumps({'matches': user.matches_()}))
        return HttpResponse(json.dumps({'matches': []}))
        
        
def adjust_min(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=GET['user_id'])
            return HttpResponse('fail')
        except User.DoesNotExist:
            user.min_score = GET['min_score']
            user.save()
            return HttpResponse('success')

        
def delete_notifications(request, id_):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        notification = {}
        if user.notification == '' or user.notification is None:
            notification['deleted'] =[str(id_)]
            notification['read'] = []
            user.notification = json.dumps(notification)
            user.save()
        else:
            notification = json.loads(user.notification)
            notification['deleted'].append(str(id_))
            user.notification = json.dumps(notification)
            user.save()
        return HttpResponse('done')
    else:
        return HttpResponse('not done')
    

def read_notifications(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        notifications = {'read': [], 'deleted':[]}
        if user.notification == None or user.notification == '':
            pass
        else:
            notifications = json.loads(user.notification)
        new_notifications = [str(x.id) for x in user.notifications() if str(x.id) not in notifications['read']]
        notifications['read'] = new_notifications + notifications['read']
        user.notification = json.dumps(notifications)
        user.save()
        return HttpResponse('done')
    else:
        return HttpResponse('not done')
    
    
def get_data(request, type_):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        if type_==  'user':
            user_data = json.loads(user.user_data)
            user_data.update(request.GET)
            user.user_data = json.dumps(user_data)
            user.save()
            return HttpResponse('success')
        
        if type_ == 'partner':
            user_data = json.loads(user.choice_data)
            user_data.update(request.GET)
            user.deal_breaker = json.dumps([user_data['dealbreaker1'], user_data['dealbreaker2']])
            del(user_data['dealbreaker1'], user_data['dealbreaker2'])
            user.choice_data = json.dumps(user_data)
            user.save()
            return HttpResponse('success')
            
        return HttpResponse('fail')    
 