from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def full_clean(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.password:
            self.set_unusable_password()
        super(User, self).full_clean(*args, **kwargs)
