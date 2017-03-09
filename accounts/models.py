from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.set_unusable_password()
