from django.contrib import admin

from accounts.models import User, OTP

admin.site.register(User)
admin.site.register(OTP)
