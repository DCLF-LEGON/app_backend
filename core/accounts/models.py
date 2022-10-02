from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        return self.fname + ' ' + self.lname if self.fname or self.lname else 'N/A'  # noqa

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email if self.email else "user"

    class Meta:
        db_table = 'user'
