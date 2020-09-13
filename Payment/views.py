import json
from decouple import config
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Account.models import User
from .models import Payment
from .ravepay_services import RavePayServices


def redirect_match(request):
    return render(request, 'Payment/match.html')


def tester(request):
    import itertools
    item = []
    item = itertools.chain(item, (x for x in [a for a in range(90)]))
    return render(request, 'Payment/test.html', {"data": item})


@csrf_exempt
@require_POST
def rave_webhook(request):
    rave_secret = request.headers.get("verify-hash")
    data = request.POST
    rave = RavePayServices({})
    payment_ = None
    try:
        payment_ = Payment.objects.get(tx_ref__exact=data['txRef'])
    except Payment.DoesNotExist:
        return
    if payment_ is not None:
        my_secret = config('RAVE_PAY_KEY')
        if rave_secret != my_secret or data['status'] != 'successful' or \
                data['currency'] != 'NGN' or data['amount'] < rave.package_price(payment_.package) \
                or payment_.payer_id != data['customer']['id']:
            payment_.status = 'FAILED'
            return HttpResponse('****')
        payment_.status = 'PAID'
        payment_.save()
        user = payment_.payer
        user.package = payment_.package
        user.save()
        return HttpResponse('**ok**')


def rave_redirect(request, user_id, package, tx_ref):
    Payment.objects.create(payer_id=user_id, package=package, tx_ref=tx_ref, date_of_payment=datetime.now())
    return render(request, 'Payment/rave_redirect.html')


def rave_pay(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        if user.package is not None:
            return redirect('redirect_match')
        else:
            return render(request, 'Payment/pay.html')
    if request.method == 'POST':
        data = request.POST
        if data['package'] == 'BASIC':
            user.package = 'BASIC'
            user.save()
            return redirect('redirect_match')
        data['user_id'] = request.user.id
        rave = RavePayServices(data)
        executed = rave.make_payment()
        if executed:
            return redirect(rave.link)
        return redirect('pay')
