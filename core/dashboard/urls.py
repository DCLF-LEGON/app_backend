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
    path('create-update-leader/', views.CreateLeaderView.as_view(), name='create-update-leader'),  # noqa
]

# preachers
urlpatterns += [
    path('preachers/', views.PreachersListView.as_view(), name='preachers'),
]

# messages
urlpatterns += [
    path('messages/', views.MessagesListView.as_view(), name='messages'),
]

# notifications
urlpatterns += [
    path('notifications/', views.NotificationsListView.as_view(), name='notifications'),  # noqa
]

# users
urlpatterns += [
    path('users/', views.UsersListView.as_view(), name='users'),
    path('create-update-user/', views.CreateUpdateUserView.as_view(), name='create_update_user'),  # noqa
]
