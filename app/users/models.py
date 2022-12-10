from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почтовый адрес', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    full_name= models.CharField('ФИО', max_length=255, null=True)
    password = models.CharField('Пароль', max_length=100)
    registration_number = models.IntegerField('Регистрационный номер', max_length=20, null=True)
    is_head = models.BooleanField('Руководитель', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

