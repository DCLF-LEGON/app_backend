from django import forms

from accounts.models import ContactUs, User
from dashboard.models import (ChurchDocument, Doctrine, Leader, Message, MessageCategory,
                              Preacher, GalleryCategory, LiveStream)


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


class GalleryCategoryForm(forms.ModelForm):
    '''Form for creating a new gallery category'''
    class Meta:
        model = GalleryCategory
        fields = ['name', 'thumbnail', ]


class ChurchDocumentForm(forms.ModelForm):
    '''Form for creating a new church document'''
    class Meta:
        model = ChurchDocument
        fields = ['title', 'document', ]


class LiveStreamForm(forms.ModelForm):
    '''Form for creating a new live stream'''
    class Meta:
        model = LiveStream
        exclude = ['created_at']


class ContactUsForm(forms.ModelForm):
    '''Form for creating a new contact us message'''
    class Meta:
        model = ContactUs
        exclude = ['created_at']