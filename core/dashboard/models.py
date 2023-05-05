import os
import random
import string
import sys
import time
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image

from accounts.models import User
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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'doctrine'


class MessageCategory(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(
        upload_to='category_thumbnails/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # crop thumbnail to 300x300
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        THUMBNAIL_SIZE = (300, 300)

        if self.thumbnail:
            image = Image.open(self.thumbnail)
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            thumb_io = BytesIO()
            image.save(thumb_io, image.format, quality=85)

            temp_name = self.thumbnail.name
            self.thumbnail.delete(save=False)

            self.thumbnail.save(
                temp_name,
                content=InMemoryUploadedFile(
                    thumb_io, None, temp_name, 'image/jpeg',
                    sys.getsizeof(thumb_io), None),
                save=False)

            super().save(*args, **kwargs)

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

    def get_likes(self):
        # returns the total likes for this message
        return LikedMessage.objects.filter(message=self).count()

    def get_media_size(self):
        if self.media:
            return f'{round(os.path.getsize(self.media.path) / 1024 / 1024, 2)} MB'  # noqa
        return '--- MB'

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'message'


class YoutubeVideo(models.Model):
    '''For storing videos fetchfed via the youtube api'''
    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.URLField()
    published_at = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class LikedMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # noqa
    message = models.ForeignKey(Message, on_delete=models.CASCADE)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'liked_message'


class RecentlyWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # noqa
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recently_watched'

    def __str__(self) -> str:
        return self.message.title


class Bookmark(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)  # noqa
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        db_table = 'bookmark'


class MessageNote(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)  # noqa
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # noqa
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.note

    class Meta:
        db_table = 'message_note'


class GeneralNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # noqa
    title = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.note

    class Meta:
        db_table = 'general_note'


class Donation(models.Model):
    def generate_transaction_id():
        time_id = str(int(time.time() * 100))
        return "".join(random.choices(string.ascii_uppercase + time_id + string.digits, k=10))
    transaction_id = models.CharField(max_length=255, primary_key=True, default=generate_transaction_id)  # noqa
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    network = models.CharField(max_length=255, null=True, blank=True)
    status_code = models.CharField(max_length=255, null=True, blank=True)
    status_message = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id if self.transaction_id else "transaction"
