from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def handler404_(request, exception):
    return render(request, '404.html', status=404)


def handler500_(request):
    return render(request, '404.html', status=500)


def handler403_(request, exception):
    return render(request, '404.html', status=403)
