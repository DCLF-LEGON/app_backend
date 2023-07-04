from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('contact-us/', views.ContactUsView.as_view(), name='contactpage'),
]
