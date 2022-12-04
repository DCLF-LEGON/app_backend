from django import forms

from accounts.models import User
from dashboard.models import Doctrine, Leader, Message, MessageCategory
from dashboard.models import Preacher


class UserForm(forms.ModelForm):
    '''Form for creating a new user'''
    class Meta:
        model = User
        fields = ['fullname', 'email', 'gender', 'phone', 'role', ]  # noqa


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


class DoctrineForm(forms.ModelForm):
    '''Form for creating a new doctrine'''
    class Meta:
        model = Doctrine
        fields = ['title', 'description', ]


class MessageCategoryForm(forms.ModelForm):
    '''Form for creating a new message category'''
    class Meta:
        model = MessageCategory
        fields = ['name', 'thumbnail', ]


class MessageForm(forms.ModelForm):
    '''Form for creating a new message'''
    class Meta:
        model = Message
        fields = ['title', 'media', 'media_type', ]  # noqa
