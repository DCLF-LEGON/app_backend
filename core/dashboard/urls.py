from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]

# donations
urlpatterns += [
    path('donations/', views.DonationsListView.as_view(), name='donations'),
]

# doctrines
urlpatterns += [
    path('doctrines/', views.DoctrinesListView.as_view(), name='doctrines'),
]

# leaders
urlpatterns += [
    path('leaders/', views.LeadersListView.as_view(), name='leaders'),
]
