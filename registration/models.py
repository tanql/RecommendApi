
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, null=True)
    userID = models.IntegerField()
    age = models.IntegerField(blank=True, null=True)
    postCode = models.CharField(max_length=20, blank=True, null=True)
