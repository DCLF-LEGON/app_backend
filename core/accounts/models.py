from django.utils import timezone
from datetime import timedelta, datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    profile_pic = models.ImageField(upload_to='profile', blank=True, null=True)  # noqa
    profile_cover = models.ImageField(upload_to='profile', blank=True, null=True)  # noqa

    created_from_dashboard = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_appuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email if self.email else 'Anonymous'  # noqa

    def resend_user_password(self):
        '''sends the user password to the user's email'''
        pass

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    # expiry_date = models.DateTimeField(default=datetime.now() + timedelta(hours=2))  # noqa

    def otp_is_expired(self):
        '''checks if the otp has expired'''
        # expiry_date = datetime.now() + timedelta(hours=2)
        expiry_date = self.created_at + timedelta(hours=2)
        if expiry_date < timezone.now():
            return True
        return False

    def send_otp(self):
        '''sends the otp to the user's email'''
        pass

    def __str__(self):
        return self.otp

    class Meta:
        db_table = 'otp'
