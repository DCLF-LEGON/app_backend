from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    profile_pic = models.ImageField(upload_to='profile', blank=True, null=True)  # noqa
    test_value = models.CharField(max_length=10, default='test')

    created_from_dashboard = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_appuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    otp_verified = models.BooleanField(default=False)

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


class MembershipInfo(models.Model):
    '''Membership information of the user'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    program = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    hall = models.CharField(max_length=150, blank=True, null=True)
    room = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.get_fullname()


class OTP(models.Model):
    '''OTP model'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def otp_is_expired(self):
        '''checks if the otp has expired'''
        expiry_date = self.created_at + timedelta(hours=2) if self.created_at else timezone.now()  # noqa
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


class ContactUs(models.Model):
    '''Contact us model'''
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact_us'
