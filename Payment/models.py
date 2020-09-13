from django.db import models
from Account.models import User


# Create your models here.

class Payment(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.CharField(choices=(('BASIC', 'BASIC'), ('CLASSIC', 'CLASSIC'), ('PREMIUM', 'PREMIUM')))
    date_of_payment = models.DateTimeField()
    status = models.CharField(choices=(('PENDING', 'PENDING'), ('PAID', 'PAID'), ('FAILED', 'FAILED')),
                              default='PENDING')
    tx_ref = models.CharField(max_length=32)
