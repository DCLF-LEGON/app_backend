from django.urls import path
from knox import views as knox_views

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.ApiEndPointsView.as_view(), name='api'),
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
    path('message-detail/', views.MessageDetailAPI.as_view(), name="msg_detail"),
    path('category-messages/', views.CategoryMessagesAPI.as_view(), name="cat_msgs"),  # noqa
    path('like-message/', views.LikeMessageAPI.as_view(), name="like_msgs"),  # noqa
]

# youtube videos
urlpatterns += [
    path('youtube-videos/', views.YoutubeVideosAPI.as_view(), name="youtube_videos"),  # noqa
    path('like-video/', views.LikeYoutubeVideoAPI.as_view(), name="like_video"),  # noqa
    path('fetch-youtube-videos/', views.FetchYoutubeDataAPI.as_view(), name="fetch_videos"),  # noqa
]


# message notes urls
urlpatterns += [
    path('create-update-message-note/', views.CreateUpdateMessageNote.as_view()),  # noqa
]


# leaders urls
urlpatterns += [
    path('leaders/', views.LeadersListAPI.as_view(), name="leaders"),
]


# preachers urls
urlpatterns += [
    path('preachers/', views.PreachersListAPI.as_view(), name="preachers"),
]

# doctrines urls
urlpatterns += [
    path('doctrines/', views.DoctrinesListAPI.as_view(), name="doctrines"),
    path('doctrine-detail/', views.DoctrineDetailAPI.as_view(), name="doctrine_detail"),  # noqa
]

# Bookmark urls
urlpatterns += [
    path('bookmarks/', views.BookmarkMessageAPI.as_view(), name="bookmarks"),
    path('add-bookmark/', views.BookmarkMessageAPI.as_view(), name="add_bookmark"),
    path('remove-bookmark/', views.RemoveBookmarkAPI.as_view(), name="remove_bookmark"),  # noqa
]

# general notes
urlpatterns += [
    path('general-notes/', views.GeneralNotesListAPI.as_view(), name="notes"),
    path('add-general-note/', views.CreateUpdateGeneralNoteAPI.as_view(), name="add_note"),  # noqa
    path('update-general-note/', views.CreateUpdateGeneralNoteAPI.as_view(), name="update_note"),  # noqa
    path('delete-note/', views.DeleteGeneralNoteAPI.as_view(), name="delete_note"),  # noqa')
]

# donations urls
urlpatterns += [
    path('make-donation/', views.MakeDonationAPI.as_view(), name="make_donation"),  # noqa
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

# Gallery
urlpatterns += [
    path('gallery/', views.GalleryAPI.as_view(), name='gallery'),
]