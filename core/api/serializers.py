from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response

from accounts.models import OTP, MembershipInfo, User
from dashboard.models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
        )
        return user


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'id')  # noqa


class MembershipInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipInfo
        exclude = ['user', ]


class MessageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCategory
        exclude = ('created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('created_at', 'updated_at')


class PreacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preacher
        exclude = ('created_at', 'updated_at')


class YoutubeVideoSerializer(serializers.ModelSerializer):
    preacher = PreacherSerializer()

    class Meta:
        model = YoutubeVideo
        exclude = ('published_at',)


class LiveStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = '__all__'


class BookmarksSerializer(serializers.ModelSerializer):
    video = YoutubeVideoSerializer()

    class Meta:
        model = Bookmark
        fields = '__all__'


class MessageNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageNote
        fields = '__all__'


class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        exclude = ('created_at', 'updated_at')


class DoctrineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctrine
        exclude = ('created_at', 'updated_at')


class GeneralNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralNote
        fields = ['id', 'title', 'note', 'created_at', ]


class DonationSerializer(serializers.ModelSerializer):
    network = serializers.CharField(max_length=20, default='MTN')
    mobile_number = serializers.CharField(max_length=15, allow_blank=True)  # noqa
    amount = serializers.DecimalField(decimal_places=3, max_digits=10)  # noqa

    class Meta:
        model = Donation
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude = ['created_at', 'category']


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        exclude = ['created_at']


class ChurchDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchDocument
        exclude = ['created_at']
