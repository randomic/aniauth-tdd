from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, email):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.set_unusable_password()
