from django.db import models
from Account.models import User


# Create your models here.

class Payment(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.CharField(max_length=10, choices=(('BASIC', 'BASIC'), ('CLASSIC', 'CLASSIC'), ('PREMIUM', 'PREMIUM')), default='BASIC')
    date_of_payment = models.DateTimeField(default=None)
    status = models.CharField(max_length=10, choices=(('PENDING', 'PENDING'), ('PAID', 'PAID'), ('FAILED', 'FAILED')),
                              default='PENDING')
    tx_ref = models.CharField(max_length=32, null=True, blank=True)
