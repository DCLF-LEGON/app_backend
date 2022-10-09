import random
import string
from dashboard.signals import generate_otp
from django.shortcuts import render
from accounts.models import OTP
from api.serializers import RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer


class ApiEndPointsView(APIView):
    def get(self, request):
        return Response({
            'sign-up': '/api/sign-up/',
            'login': '/api/login/',
            'user-profile': '/api/user-profile/',

            'verify-otp': '/api/verify-otp/',
            'resend-otp': '/api/resend-otp/',
        })


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class SignUpAPI(generics.GenericAPIView):
    '''This CBV is used to register a new user'''
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)


class VerifyOTPAPI(generics.GenericAPIView):
    '''This CBV is used to verify a user's OTP'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp')
        token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        if token_key:
            token = AuthToken.objects.get(token_key=token_key)
            user = token.user
            otp = OTP.objects.filter(user=user, otp=otp_code).first()
            if otp and (otp.otp_is_expired() == False):
                otp.delete()
                return Response({
                    "message": "OTP verified successfully",
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Invalid OTP!",
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)


class ResendOTPAPI(generics.GenericAPIView):
    '''This CBV is used to resend a user's OTP'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        if token_key:
            token = AuthToken.objects.filter(token_key=token_key).first()
            if token:
                user = token.user
            else:
                return Response({
                    "message": "Invalid token!",
                }, status=status.HTTP_400_BAD_REQUEST)
            otp = OTP.objects.filter(user=user).first()
            if otp:
                otp.delete()
            # The create function will create a new OTP
            # and trigger a signal that will send the OTP to the user's mail
            otp = OTP.objects.create(user=user, otp=generate_otp())
            return Response({
                "message": f"OTP resent successfully to {otp.user.email}",
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid token!",
        }, status=status.HTTP_400_BAD_REQUEST)
