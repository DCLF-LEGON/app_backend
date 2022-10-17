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
    path('create-update-leader/', views.CreateLeaderView.as_view(), name='create_update_leader'),  # noqa
    path('leader-details/', views.LeaderDetailsView.as_view(), name='leader_details'),  # noqa
    path('search-leader/', views.SearchLeaderView.as_view(), name='search_leader'),  # noqa
    path('delete-leader/', views.DeleteLeaderView.as_view(), name='delete_leader'),  # noqa
]

# preachers
urlpatterns += [
    path('preachers/', views.PreachersListView.as_view(), name='preachers'),
    path('create-update-preacher/', views.CreatePreacherView.as_view(), name='create_update_preacher'),  # noqa
    path('preacher-details/', views.PreacherDetailsView.as_view(), name='preacher_details'),  # noqa
    path('search-preacher/', views.SearchPreacherView.as_view(), name='search_preacher'),  # noqa
    path('delete-preacher/', views.DeletePreacherView.as_view(), name='delete_preacher'),  # noqa
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
    path('user-details/', views.UserDetailsView.as_view(), name='user_details'),
    path('search-user/', views.SearchUsersView.as_view(), name='search_user'),
    path('delete-user/', views.DeleteUserView.as_view(), name='delete_user'),
]
