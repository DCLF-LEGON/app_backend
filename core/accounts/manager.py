from django.contrib.auth.models import BaseUserManager
from core.utils.constants import UserRoles


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, fname, lname, **kwargs):
        user = self.model(email=email, password=password,
                          fname=fname, lname=lname, **kwargs)
        user.set_password(password)
        user.is_appuser = True
        user.role = UserRoles.app_user.value
        user.save()
        return user

    def create_superuser(self, email, password, fname, lname, **kwargs):
        user = self.create_user(email,  password, fname, lname, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
