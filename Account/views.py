from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from .models import User
import json
from .algorithms import get_username, match_user
from Chat.algorithms import in_my_chat, create_private_key
from Chat.models import ChatThread
import datetime
from django.core.mail import send_mail


# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = auth.authenticate(
                request, username=email, password=password)
            if user is None:
                return redirect('not_found')
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

            # if user is not None and user.verified  == False:
            #     if 'verified' in request.session and request.session['email'] == email:
            #         del request.session['verified'], request.session['email']
            #         user.verified = True
            #         user.save()
            #         auth.login(request, user)
            #         return redirect('dashboard')

            # request.session['code'] = request.POST['csrfmiddlewaretoken'] link = f'http://{request.get_host(
            # )}/account/verify/?code={request.POST["csrfmiddlewaretoken"]}?email={email}' message = f''' Dear {
            # user.first_name}, \n We are excited to have you on Datefix. Below is the link to verify your email
            # address, click on this link to continue.\n \n {link} \n

            #     If you have no account with Datefix, please ignore.

            #     Cheers,
            #     Datefix Team.
            #     '''
            #     send_mail('Email Verification', message, 'admin@datefix.me', [email])
            #     return redirect('verification')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
    return render(request, 'Account/login.html')


def test(request):
    return render(request, 'Account/test.html')


def results(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        matches = None
        if user.sex == 'female':
            matches = user.successful_list()
        if user.sex == 'male':
            matches = user.matches_()
        select = [[x[0][0], x[1][1]] for x in matches]
        return render(request, 'Account/results.html',
                      {'matches': matches, "select": select, "matches_length": len(matches)})
    if request.method == 'POST':
        selected = request.POST['matches']
        success = user.successful_list()
        for i in selected:
            if User.objects.get(id=int(i)).complete_match():
                continue
            success = [x for x in success if x[0][1] != i]
            user.successful_matches = json.dumps(success)
            user.matches = json.dumps(selected)
            user.save()
            # add user to match chatters
            user_ = user.objects.get(id=int(i))
            user_.matches = json.loads(user_.matches).append(user.id)
            user_.save()
            chat = ChatThread()
            chat.first_user = user
            chat.second_user = user_
            chat.secret = create_private_key()
            chat.date_created = datetime.datetime.now()
            chat.save()
            selected.remove(i)
            return redirect('chatroom')
        if len(selected) > 0:
            match_comp = [x[1][1] for x in success if x[0][1] in selected]
            verb = 'has'
            if len(selected) > 1:
                verb = 'have'
            request.session['message'] = f'{"and ".join(match_comp)} {verb} complete matches, so choose another.'
            request.session['staus'] = 'info'
            return redirect('results')
        return redirect('chatroom')


def signup(request):
    if request.method == 'POST':
        if not (request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != ''):
            return redirect('login')

        try:
            User.objects.get(email=request.POST['email'])
            return redirect('login')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=get_username(),
                email=request.POST['email'],
                password=request.POST['password1'],
                first_name=request.POST['first-name'],
                last_name=request.POST['last-name'],
                sex=request.POST['sex'],
                phone=request.POST['phone']
            )
            user.save()
            return redirect('login')

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, 'Account/login.html')


def dashboard(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('login')

        user = User.objects.get(id=request.user.id)

        if user.user_data is None or user.user_data == '':
            return render(request, 'Account/profile.html')

        if not user.complete_match() and not (user.user_data is None or user.user_data == ''):
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


def adjust_min(request):
    user = None
    if request.method == 'GET':
        try:
            user = User.objects.get(id=request.GET['user_id'])
            return HttpResponse('fail')
        except User.DoesNotExist:
            user.min_score = request.GET['min_score']
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
        if user.notification is None or user.notification == '':
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
            user.user_data = "{}"
            user.save()
        if user.choice_data is None or user.choice_data == '':
            user.choice_data = "{}"
            user.save()

        if type_ == 'user':
            user_data = json.loads(user.user_data)
            user_data.update(request.GET)
            user.user_data = json.dumps(user_data).replace(
                ']', '').replace('[', '')
            user.save()
            return HttpResponse('success')

        if type_ == 'partner':
            user_data = json.loads(user.choice_data)
            user_data.update(request.GET)
            user.deal_breaker = "[" + json.dumps(
                [user_data['dealbreaker1'], user_data['dealbreaker2']]).replace(']', '').replace('[', '') + "]"
            del (user_data['dealbreaker1'], user_data['dealbreaker2'])
            user.choice_data = json.dumps(
                user_data).replace(']', '').replace('[', '')
            user.save()
            return HttpResponse('success')

        return HttpResponse('fail')


def verified(request):
    return render(request, 'Account/account-verified.html')


def verify(request):
    if request.method == 'GET' and 'code' in request.session:
        if request.session['code'] == request.GET['code']:
            del request.session['code']
            request.session['verified'] = True
            request.session['email'] = request.GET['email']
            return redirect('verification')
    return redirect('login')


def not_found(request):
    return render(request, 'Account/account-not-found.html')


def verification(request):
    return render(request, 'Account/verification-link-sent.html')
