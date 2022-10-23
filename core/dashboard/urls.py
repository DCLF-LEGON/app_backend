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
    path('search-donation/', views.SearchDonationView.as_view(), name='search-donation'),  # noqa
]

# doctrines
urlpatterns += [
    path('doctrines/', views.DoctrinesListView.as_view(), name='doctrines'),
    path('create-update-doctrine/', views.CreateUpdateDoctrineView.as_view(), name='create_update_doctrine'),  # noqa
    path('doctrine-details/', views.DoctrineDetailsView.as_view(), name='doctrine_details'),  # noqa
    path('search-doctrine/', views.SearchDoctrineView.as_view(), name='search_doctrine'),  # noqa
    path('delete-doctrine/', views.DeleteDoctrineView.as_view(), name='delete_doctrine'),  # noqa
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
    path('create-update-message/', views.CreateUpdateMessageView.as_view(), name='create_update_message'),  # noqa
    path('message-details/', views.MessageDetailsView.as_view(), name='message_details'),  # noqa
    path('search-message/', views.SearchMessageView.as_view(), name='search_message'),  # noqa
    path('delete-message/', views.DeleteMessageView.as_view(), name='delete_message'),  # noqa
]

# messages category
urlpatterns += [
    path('categories/', views.CategoriesListView.as_view(), name='categories'),
    path('create-update-category/', views.CreateUpdateCategoryView.as_view(), name='create_update_category'),  # noqa
    path('message-details/', views.MessageDetailsView.as_view(), name='message_details'),  # noqa
    path('search-category/', views.SearchCategoryView.as_view(), name='search_category'),  # noqa
    path('delete-category/', views.DeleteCategoryView.as_view(), name='delete_category'),  # noqa
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
