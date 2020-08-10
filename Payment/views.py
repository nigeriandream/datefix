from django.shortcuts import render, redirect

# Create your views here.
from Account.models import User


def payment(request):
    user = User.objects.get(id=request.user.id)
    if user.payed:
        pass
    else:
        # pay money
        pass
    return render(request, 'Payment/payment.html')


def test(request):
    if request.method == 'GET':
        if 'girls' in request.GET:
            print ((request.GET['girls']).split(','))
            from django.http import HttpResponse
            import json
            return HttpResponse(json.dumps(str(request.GET['girls']).split(',')))
        else:
            return render(request, 'Payment/test.html')

