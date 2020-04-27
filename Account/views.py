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
        if not request.POST['choice'] and request.POST['password1'] == request.POST['password2'] :
            my_data = request.POST
            user = User.objects.create_user(
                username= get_username(),
                email = request.POST['email'],
                password = request.POST['password1']
            )
            user.user_data = json.dumps(request.POST)
            user.save()
            request.session['choice'] = True
            request.session['user_id'] = user.id
            return redirect('signup')
        else:
            user = User.objects.get(id=request.session['user_id'])
            user.choice_data = json.dumps(request.POST)
            user.save()
            return redirect('data_details')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        if request.session.get('choice', False):
            del request.session['choice']
            request.session['deal_breaker'] = True
            return render(request, 'Account/signup.html', {'choice': True})
        else:
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
            return render(request, 'Account/profile.html', {'user_details': user_details,
                                                              'choice_details': choice_details,
                                                              'matches': matches,
                                                              'notifications': notifications,
                                                              'new_notification': user.new_notifications(),
                                                              'accepted': accepted})
        else:
            return redirect('login')

def data_details(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        if request.session.get('deal_breaker', False):
            del request.session['deal_breaker']
            data = list(json.loads(user.choice_data))
            return render(request, 'Account/final.html', {'attributes': data})
        elif request.session.get('change min', False):
            return render(request, 'Account/final.html', {'adjust': True})
        else:
            return redirect('signup')
    elif request.method == 'POST':
        if request.session['change min']:
            user.min_score = request.POST['minimum score']
            user.save()
            del request.session['change min']
            return redirect('match')
        else:
            user.deal_breaker = ' , '.join(list(request.POST)[1:3])
            user.profile_picture = request.FILES['profile_pic']
            user.min_score = request.POST['minimum score']
            user.save()
            return redirect('payment')
        
    
def update_profile(request):
    pass
    # the post form for updating profile and new payment
    return redirect ('dashboard')

def matching(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if match_user(user) is True:
            return redirect('dashboard')
        else:
            request.session['change min'] = True
            return redirect('data_details')
        
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
    
    

        