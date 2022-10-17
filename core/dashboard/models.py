from accounts.models import User
from tkinter import Image
from django.db import models


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
