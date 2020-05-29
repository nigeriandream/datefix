from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from .models import User
import json
from .algorithms import get_username, match_user
from Chat.algorithms import in_my_chat, create_private_key
from Chat.models import Chat_Thread
import datetime
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


def results(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        matches = user.successful_list()
        select = [[x[0][0], x[1][1]] for x in matches]
        return render(request, 'Account/results.html', {'matches': matches, "select": select, "matches_length": len(matches)})
    if request.method == 'POST':
        selected = request.POST['matches']
        success = user.successful_list()
        success = [x for x in success if x[0][1] not in selected]
        user.successful_matches = json.dumps(success)
        user.matches = json.dumps(selected)
        user.save()
        for i in selected:
            chat = Chat_Thread()
            chat.first_user = user
            chat.second_user = User.objects.get(id=int(i))
            chat.secret = create_private_key()
            chat.date_created = datetime.datetime.now()
            chat.save()
        return redirect('chatroom')


def forgotpassword(request):
    return render(request, 'Account/forgotpassword.html')


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != '' :
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
        if not  request.user.is_authenticated:
            return redirect('login')

        user = User.objects.get(id=request.user.id)

        if user.user_data is None or user.user_data == '':
                return render(request, 'Account/profile.html')
        
        
        if (not user.complete_match() and not(user.user_data is None or user.user_data == '')):
            user = User.objects.get(id=request.user.id)
            user_details = user.user_data_()
            user_details['registered'] = True
            return render(request, 'Account/profile.html', user_details)
        


def matching(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        if user.sex == 'female':
            match_user(user)
            return redirect('results')
    return redirect('dashboard')


def adjust_min(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=request.GET['user_id'])
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
            notification['deleted'] = [str(id_)]
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
        notifications = {'read': [], 'deleted': []}
        if user.notification == None or user.notification == '':
            pass
        else:
            notifications = json.loads(user.notification)
        new_notifications = [str(x.id) for x in user.notifications() if str(
            x.id) not in notifications['read']]
        notifications['read'] = new_notifications + notifications['read']
        user.notification = json.dumps(notifications)
        user.save()
        return HttpResponse('done')
    else:
        return HttpResponse('not done')


def get_data(request, type_):
    if request.method == 'GET':
        print(request.GET)
        user = User.objects.get(id=request.user.id)
        if user.user_data is None or user.user_data == '':
            user.user_data =  "{}"
            user.save()
        if user.choice_data is None or user.choice_data == '':
            user.choice_data =  "{}"
            user.save()
        
        if type_ == 'user':
            user_data = json.loads(user.user_data)
            user_data.update(request.GET)
            user.user_data = json.dumps(user_data).replace(']', '').replace('[', '')
            user.save()
            return HttpResponse('success')

        if type_ == 'partner':
            user_data = json.loads(user.choice_data)
            user_data.update(request.GET)
            user.deal_breaker = "["+json.dumps(
                [user_data['dealbreaker1'], user_data['dealbreaker2']]).replace(']', '').replace('[', '')+"]"
            del(user_data['dealbreaker1'], user_data['dealbreaker2'])
            user.choice_data = json.dumps(user_data).replace(']', '').replace('[', '')
            user.save()
            return HttpResponse('success')

        return HttpResponse('fail')
