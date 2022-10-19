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


# categories urls
urlpatterns += [
    path('categories/', views.MessageCategoriesListAPI.as_view(), name="categories"),  # noqa
]

# messages urls
urlpatterns += [
    path('all-messages/', views.MessagesListAPI.as_view(), name="all_msgs"),
    path('category-messages/', views.CategoryMessagesAPI.as_view(), name="cat_msgs"),  # noqa
]

# API AUTHENTICATION (login, logout, etc.)
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # noqa
]

# UPDATE PROFILE
urlpatterns += [
    path('user-profile/', views.UserProfileAPI.as_view(), name='user_profile'),  # noqa
    path('change-password/', views.ChangePasswordAPI.as_view(), name='change_password'),  # noqa
]
