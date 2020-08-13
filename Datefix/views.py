from django.shortcuts import render

# Create your views here.
from Account.models import User


def home(request):
    if 'email' in request.session:
        del request.session['email']
    if 'category' in request.session:
        del request.session['category']
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        return render(request, 'home.html', {'user': user})
    return render(request, 'home.html')


def handler404_(request, exception):
    return render(request, '404.html', status=404)


def handler500_(request):
    return render(request, '404.html', status=500)


def handler403_(request, exception):
    return render(request, '404.html', status=403)
