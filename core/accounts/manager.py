from django.contrib.auth.models import BaseUserManager

from core.utils.constants import UserRoles


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, fullname='-', **kwargs):
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_appuser = True
        user.role = UserRoles.app_user.value
        user.save()
        return user

    def create_superuser(self, email, password, fullname='-', **kwargs):
        user = self.create_user(
            email,  password, fullname='-', **kwargs)
        user.is_superuser = True
        user.role = UserRoles.administrator.value
        user.is_staff = True
        user.save()
        return user
