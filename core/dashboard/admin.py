from django.contrib import admin

from accounts.models import OTP, MembershipInfo, User
from dashboard.models import YoutubeVideo, MessageCategory, Preacher, Leader, Doctrine, Message, Gallery, GalleryCategory, GeneralNote

admin.site.register(User)
admin.site.register(OTP)
admin.site.register(YoutubeVideo)
admin.site.register(MessageCategory)
admin.site.register(Preacher)
admin.site.register(Leader)
admin.site.register(Doctrine)
admin.site.register(Message)
admin.site.register(Gallery)
admin.site.register(GalleryCategory)
admin.site.register(GeneralNote)
admin.site.register(MembershipInfo)
