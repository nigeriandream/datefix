from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from .models import User, PersonalityTest
import json
from .algorithms import get_username, match_user, flash, display, send_verification
from Chat.algorithms import create_chat


# Create your views here.

# login function verified
def login(request):
    if request.method == 'POST':
        if not request.POST.get('email', False) or not request.POST.get('password', False):
            flash(request, 'No login details was entered !', 'danger', 'remove-sign')
            return redirect('login')
        try:
            user = User.objects.get(email=request.POST['email'])

            if not user.verified:
                send_verification(request)
                return redirect('verification')

            user = auth.authenticate(
                request, username=request.POST['email'], password=request.POST['password'])
            if user is None:
                flash(request, 'Password Incorrect !', 'danger', 'remove-sign')
                return redirect('login')
            if user is not None:
                auth.login(request, user)
                flash(request, f'{user.username} is logged in successfully !', 'success', 'thumbs-up')
                return redirect('dashboard')
        except User.DoesNotExist:
            flash(request, 'There is no Account with this email address !', 'info', 'info-sign')
            return redirect('not_found')

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        flash_ = display(request)
        if flash_ is None:
            return render(request, 'Account/login.html')
        return render(request, 'Account/login.html', {'message': flash_[0], 'status': flash_[1], "icon": flash_[2]})


def personality(request):
    if request.method == 'GET':
        test_ = PersonalityTest()
        try:
            test_ = PersonalityTest.objects.get(email=request.GET['email'])
        except PersonalityTest.DoesNotExist:
            test_.email = request.GET['email']
        test_.personalities = request.GET['personality']
        test_.scores = request.GET['score']
        test_.save()
        return HttpResponse('Personality Test Taken')


# verified
def results(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        matches = None
        if user.sex == 'female':
            matches = user.successful_list()
            select = [[x[0][0], x[1][1]] for x in matches]
            return render(request, 'Account/results.html',
                          {'matches': matches, "select": select, "matches_length": len(matches)})
        if user.sex == 'male':
            matches = [User.objects.get(id=x) for x in user.matches_()]
            return render(request, 'Account/results_m.html',
                          {'matches': matches, "matches_length": len(matches)})

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
            match_list = json.loads(user_.matches)
            match_list.append(user.id)
            user_.matches = json.dumps(match_list)
            user_.save()
            create_chat(user, user_)
            # send notification to both partners
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


# signup verified
def signup(request):
    if request.method == 'POST':
        if not (request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != ''):
            flash(request, 'The passwords are not equal !', 'danger', 'remove-sign')
            return redirect('login')

        if not request.POST.get('email', False) or not request.POST.get('last-name', False) or not request.POST.get(
                'first-name', False):
            flash(request, 'Some Fields are empty !', 'danger', 'remove-sign')
            return redirect('login')

        try:
            User.objects.get(email=request.POST['email'])
            flash(request, 'This email already exists !', 'danger', 'remove-sign')
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
            flash(request, f"{request.POST['first-name']}, your account has been "
                           f"created successfully.", 'success', 'thumbs-up')
            return redirect('login')

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        flash_ = display(request)
        if flash_ is None:
            return render(request, 'Account/login.html')
        return render(request, 'Account/login.html', {'message': flash_[0], 'status': flash_[1], 'icon': flash_[2]})


# verified
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
        if user.complete_match():
            return redirect('chatroom')


# verified
def matching(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        if user.sex == 'female':
            matched = match_user(user)
            if not matched:
                return HttpResponse('fail')

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


# verified
def get_data(request, type_):
    if request.method == 'GET':
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


# verified
def verified(request):
    return render(request, 'Account/account-verified.html')


# verify function is verified
def verify(request):
    if request.method == 'POST':
        flash(request, 'Invalid Request !', 'danger')
        return redirect('login')

    if 'code' not in request.session:
        flash(request, 'Code has expired !', 'danger', 'remove-sign')
        return redirect('login')

    del request.session['code']
    request.session['verified'] = True
    request.session['email'] = request.GET['email']
    return redirect('verification')


# verified
def not_found(request):
    return render(request, 'Account/account-not-found.html')


# verified
def verification(request):
    return render(request, 'Account/verification-link-sent.html')


# verified
def test(request):
    return render(request, 'Account/test.html')
