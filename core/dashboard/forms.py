from django import forms

from accounts.models import User


class UserForm(forms.ModelForm):
    '''Form for creating a new user'''
    class Meta:
        model = User
        fields = ['fullname', 'email', 'gender', 'phone', 'dob', 'region', 'city', 'zip', 'country', 'role', ]  # noqa
