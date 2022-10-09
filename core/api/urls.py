from knox import views as knox_views
from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('api/', views.ApiEndPointsView.as_view(), name='api'),
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
]


# otp urls
urlpatterns += [
    path('verify-otp/', views.VerifyOTPAPI.as_view(), name="verify_otp"),
    path('resend-otp/', views.ResendOTPAPI.as_view(), name="resend_otp"),
]


# API AUTHENTICATION (login, logout, etc.)
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # noqa
]
