from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]

# donations
urlpatterns += [
    path('donations/', views.DonationsListView.as_view(), name='donations'),
    path('search-donation/', views.SearchDonationView.as_view(), name='search-donation'),  # noqa
    path('download-as-csv/', views.DownloadDonationsAsCSV.as_view(), name='download_as_csv'),  # noqa
    path('download-as-xl/', views.DownloadDonationsAsExcel.as_view(), name='download_as_xl'),  # noqa
    path('download-as-pdf/', views.DownloadDonationsAsPDF.as_view(), name='download_as_pdf'),  # noqa
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

# Youtube videos
urlpatterns += [
    path('youtube-videos/', views.YoutubeVideosView.as_view(), name='youtube_videos'),  # noqa
    path('search-youtube-video/', views.SearchYoutubeVideoView.as_view(), name='search_yt_video'),  # noqa
    path('delete-youtube-video/', views.DeleteYoutubeVideoView.as_view(), name='delete_yt_video'),  # noqa
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
    path("add-user-to-group/", views.AddUserToGroupsView.as_view(), name="add_user_to_group"),  # noqa
    path("add-perms-to-user/", views.AddPermsToUserView.as_view(), name="add_perms_to_user"),  # noqa
]

# profile urls
urlpatterns += [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update-profile/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
]


# Groups
urlpatterns += [
    path("groups/", views.GroupsListView.as_view(), name="groups"),
    path("create-update-group/", views.CreateUpdateGroupView.as_view(), name="create_update_group"),  # noqa
    path("search-group/", views.SearchGroupView.as_view(), name="search_group"),  # noqa
    path("delete-group/", views.DeleteGroupView.as_view(), name="delete_group"),  # noqa
    path('add-perms/', views.AddPermissionsToGroupView.as_view(), name='add_perms'),  # noqa
]
