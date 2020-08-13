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


def tester(request):
    import itertools
    item = []
    item = itertools.chain(item, (x for x in [a for a in range(90)]))
    return render(request, 'Payment/test.html', {"data": item})
