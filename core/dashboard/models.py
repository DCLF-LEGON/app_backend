import os
from accounts.models import User
from django.db import models

from core.utils.constants import MediaType


class Leader(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='assets/leader_pics/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'leader'


class Preacher(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='assets/preacher_pics/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'preacher'


class Doctrine(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='doctrines', on_delete=models.CASCADE)  # noqa
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'doctrine'


class MessageCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Message(models.Model):
    title = models.CharField(max_length=200)
    media = models.FileField(upload_to='assets/messages/', blank=True, null=True)  # noqa
    media_type = models.CharField(max_length=10, choices=(
        (MediaType.audio.value, MediaType.audio.value),
        (MediaType.video.value, MediaType.video.value),
    ), default=MediaType.video.value)
    preacher = models.ForeignKey(Preacher, related_name='messages', on_delete=models.CASCADE)  # noqa
    category = models.ForeignKey(MessageCategory, related_name='messages', on_delete=models.CASCADE)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_media_size(self):
        if self.media:
            return f'{round(os.path.getsize(self.media.path) / 1024 / 1024, 2)} MB'  # noqa
        return '--- MB'

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'message'
