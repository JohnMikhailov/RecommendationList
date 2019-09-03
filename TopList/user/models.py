from django.db import models
from django.contrib.auth.models import User, UserManager


class CustomUserManager(UserManager):

    def create(self, **obj_data):
        return super().create_user(**obj_data)


class CustomUser(User):

    refresh_token = models.CharField(max_length=500, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatars', null=True)

    objects = CustomUserManager()
