from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField("Локация", max_length=30)
    age = models.IntegerField()
    mail = models.EmailField(max_length=50, blank=True)# не обязательное поле к заполнению

    def __str__(self):
        return self.user.username


class Address(models.Model):

    choice = models.BooleanField("", default = False)
    number = models.PositiveSmallIntegerField()
    name = models.CharField("", max_length = 50)

    def __str__(self):
        return self.name