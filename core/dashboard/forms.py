from django import forms

from accounts.models import User
from dashboard.models import Leader
from dashboard.models import Preacher


class UserForm(forms.ModelForm):
    '''Form for creating a new user'''
    class Meta:
        model = User
        fields = ['fullname', 'email', 'gender', 'phone', 'dob', 'region', 'city', 'zip', 'country', 'role', ]  # noqa


class LeaderForm(forms.ModelForm):
    '''Form for creating a new leader'''
    class Meta:
        model = Leader
        fields = ['name', 'title', 'position', 'picture', ]


class PreacherForm(forms.ModelForm):
    '''Form for creating a new preacher'''
    class Meta:
        model = Preacher
        fields = ['name', 'title', 'position', 'picture', ]
