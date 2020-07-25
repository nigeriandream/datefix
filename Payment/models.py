from django.db import models
from Account.models import User


# Create your models here.

class Payment(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
