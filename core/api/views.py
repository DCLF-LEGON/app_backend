import decimal
import os
import random
import string
import time

import google.auth
from django.contrib.auth import login
from googleapiclient.discovery import build
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

import core.settings as settings
from accounts.models import OTP
from api import serializers
from api.serializers import (MessageCategorySerializer, RegisterSerializer,
                             UserSerializer, YoutubeVideoSerializer)
from core import settings
from core.utils.util_functions import (fetch_youtube_data,
                                       get_transaction_status, receive_payment)
from dashboard.models import (Bookmark, Doctrine, Donation, Gallery, GeneralNote,
                              Leader, LikedMessage, Message, MessageCategory,
                              MessageNote, Preacher, RecentlyWatched, YoutubeVideo)
from dashboard.signals import generate_otp

from .serializers import (DoctrineSerializer, DonationSerializer, GallerySerializer,
                          GeneralNoteSerializer, LeaderSerializer,
                          MessageNoteSerializer, OTPSerializer,
                          PreacherSerializer)


class ApiEndPointsView(APIView):
    def get(self, request):
        return Response({
            'sign-up': '/api/sign-up/',
            'login': '/api/login/',
            'user-profile': '/api/user-profile/',

            'verify-otp': '/api/verify-otp/',
            'resend-otp': '/api/resend-otp/',
            'user-profile': '/api/user-profile/',
        })


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # check if user has verified their otp
        if not user.otp_verified:
            return Response({
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1],
            }, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        # Delete token
        AuthToken.objects.filter(user=user).delete()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_200_OK)


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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        otp_code = request.data.get('otp')
        otp = OTP.objects.filter(user=user, otp=otp_code).first()
        if otp and (otp.otp_is_expired() == False):
            otp.delete()
            user.otp_verified = True
            user.save()
            return Response({
                "message": "OTP verified successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid OTP!",
            }, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPAPI(generics.GenericAPIView):
    '''This CBV is used to resend a user's OTP'''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        otp = OTP.objects.filter(user=user).first()
        if otp:
            otp.delete()
        # The create function will create a new OTP
        # and trigger a signal that will send the OTP to the user's mail
        otp = OTP.objects.create(user=user, otp=generate_otp())
        return Response({
            "message": f"OTP resent successfully to {otp.user.email}",
        }, status=status.HTTP_200_OK)


class ChangePasswordAPI(APIView):
    '''This CBV is used to change a user's password'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({
            "message": "Password Changed Successfully",
        }, status=status.HTTP_200_OK)


class UserProfileAPI(APIView):
    '''This CBV is used to get a user's profile'''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "user": UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class MessageCategoriesListAPI(APIView):
    '''This CBV is used to get all categories'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        categories = MessageCategory.objects.all()
        return Response({
            "categories": MessageCategorySerializer(categories, many=True).data,
        }, status=status.HTTP_200_OK)


class YoutubeVideosAPI(APIView):
    '''CBV for getting all the youtube video fetched via api'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        videos = YoutubeVideo.objects.all().filter().order_by('-published_at')
        return Response({
            "videos": YoutubeVideoSerializer(videos, many=True).data,
        }, status=status.HTTP_200_OK)


class LikeYoutubeVideoAPI(APIView):
    '''CBV for like a youtube video'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        video = YoutubeVideo.objects.filter(video_id=video_id).first()
        if video:
            video.likes += 1
            video.save()
            return Response({
                "message": "Video Liked!",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Ooops!",
            }, status=status.HTTP_404_NOT_FOUND)


class BookmarkYoutubeVideoAPI(APIView):
    '''CBV for bookmarking a youtube video'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        video = YoutubeVideo.objects.filter(video_id=video_id).first()
        if video:
            Bookmark.objects.create(video=video, user=request.user)
            return Response({
                "message": "Video Saved!",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Ooops!",
            }, status=status.HTTP_404_NOT_FOUND)


class FetchYoutubeDataAPI(APIView):
    '''CBV for fetching youtube data'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        videos = fetch_youtube_data(settings.CHANNEL_ID)
        videos2 = fetch_youtube_data(settings.CHANNEL_ID2)
        videos.extend(videos2)
        videos_saved = 0
        for video in videos:
            # check if video already exists in YoutubeVideo model
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"].strip().replace("\n", "").replace("||", "")  # noqa
            description = video["snippet"]["description"]
            thumbnailUrl = video["snippet"]["thumbnails"]["high"]["url"]
            published_at = video["snippet"]["publishedAt"]
            existing_video = YoutubeVideo.objects.filter(video_id=video_id).first()  # noqa
            if existing_video is None:
                YoutubeVideo.objects.create(
                    video_id=video_id,
                    title=title,
                    description=description,
                    thumbnail_url=thumbnailUrl,
                    published_at=published_at
                )
                videos_saved += 1
        return Response({
            "message": "Youtube Videos Fetched Successfully",
            "videos_saved": videos_saved,
            "videos": videos,
        }, status=status.HTTP_200_OK)


class MessagesListAPI(APIView):
    '''This CBV is used to get all messages from all categories'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        messages = Message.objects.all().order_by('-created_at')

        all_messages = []
        for message in messages:
            all_messages.append({
                "id": message.id,  # type: ignore
                "title": message.title,
                "media": message.media.url,
                "media_type": message.media_type.upper(),
                "category": message.category.name.upper(),
                "preacher": message.preacher.title.upper() + '. ' + message.preacher.name.upper(),
            })
        return Response({
            "messages": all_messages,
        }, status=status.HTTP_200_OK)


class MessageDetailAPI(APIView):
    '''This CBV is used to get a message's details'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        message_id = request.data.get('message_id')
        message = Message.objects.filter(id=message_id).first()
        user = None
        if request.user.is_authenticated:
            user = request.user
            notes = MessageNote.objects.filter(message=message, user=user).order_by('-created_at')  # noqa
            message_notes = MessageNoteSerializer(notes, many=True).data
        else:
            message_notes = []
        if message:
            result = {
                "id": message.id,  # type: ignore
                "title": message.title,
                "media": message.media.url,
                "media_type": message.media_type.upper(),
                "category": message.category.name.upper(),
                "preacher": message.preacher.title.upper() + '. ' + message.preacher.name.upper(),
                "created_at": message.created_at,
                "likes": message.get_likes(),
                "notes": message_notes,
            }
            # create a recently watched object
            try:
                RecentlyWatched.objects.create(user=user, message=message)
            except:
                pass
            return Response({
                "message": result,
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Message not found!",
        }, status=status.HTTP_404_NOT_FOUND)


class LikeMessageAPI(APIView):
    '''This CBV is used to like a message'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        message_id = request.data.get('message_id')
        message = Message.objects.filter(id=message_id).first()
        if message:
            like = LikedMessage.objects.filter(
                user=user, message=message).first()
            if like:
                like.delete()
                return Response({
                    "message": "Message unliked successfully",
                }, status=status.HTTP_200_OK)
            else:
                LikedMessage.objects.create(user=user, message=message)
                return Response({
                    "message": "Message liked successfully",
                }, status=status.HTTP_200_OK)
        return Response({
            "message": "Message not found!",
        }, status=status.HTTP_404_NOT_FOUND)


class CreateUpdateMessageNote(APIView):
    '''This CBV is used to create or update a message note'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        message_id = request.data.get('message_id')
        note = request.data.get('note')
        message = Message.objects.filter(id=message_id).first()
        if message:
            message_note = MessageNote.objects.filter(
                user=user, message=message).first()
            if message_note:
                # if message note already exists, update it
                message_note.note = note
                message_note.save()
                return Response({
                    "message": "Note Updated Successfully",
                }, status=status.HTTP_200_OK)
            else:
                # if message note does not exist, create it
                MessageNote.objects.create(
                    user=user, message=message, note=note)
                return Response({
                    "message": "Note Created Successfully",
                }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Message not found!",
        }, status=status.HTTP_404_NOT_FOUND)


class CategoryMessagesAPI(APIView):
    '''This CBV is used to get all messages from specified category'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        category = MessageCategory.objects.filter(pk=category_id).first()
        if not category:
            return Response({
                "message": "Invalid category!",
            }, status=status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.filter(category=category).order_by('-created_at')  # noqa
        all_messages = []
        for message in messages:
            all_messages.append({
                "id": message.pk,
                "title": message.title,
                "media": message.media.url,
                "media_type": message.media_type.upper(),
                "category": message.category.name.upper(),
                "preacher": message.preacher.title.upper() + '. ' + message.preacher.name.upper(),
            })
        return Response({
            "messages": all_messages,
        }, status=status.HTTP_200_OK)


class CategoryYoutubeMessagesAPI(APIView):
    '''This CBV is used to get all youtube messages from specified category'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        category_id = request.data.get('category_id')
        category = MessageCategory.objects.filter(id=category_id).first()
        messages = YoutubeVideo.objects.filter(category=category).order_by('-published_at')  # noqa
        serializer = YoutubeVideoSerializer(messages, many=True)
        return Response({
            "messages": serializer.data,
        }, status=status.HTTP_200_OK)


class LeadersListAPI(APIView):
    '''This CBV is used to get all leaders'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        leaders = Leader.objects.all().order_by('-created_at')
        return Response({
            "leaders": LeaderSerializer(leaders, many=True).data,
        }, status=status.HTTP_200_OK)


class PreachersListAPI(APIView):
    '''This CBV is used to get all preachers'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        preachers = Preacher.objects.all().order_by('-created_at')
        return Response({
            "preachers": PreacherSerializer(preachers, many=True).data,
        }, status=status.HTTP_200_OK)


class DoctrinesListAPI(APIView):
    '''This CBV is used to get all doctrines'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctrines = Doctrine.objects.all().order_by('-created_at')
        return Response({
            "doctrines": DoctrineSerializer(doctrines, many=True).data,
        }, status=status.HTTP_200_OK)


class DoctrineDetailAPI(APIView):
    '''This CBV is used to get a doctrine's details'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        doctrine_id = request.data.get('doctrine_id')
        doctrine = Doctrine.objects.filter(id=doctrine_id).first()
        if doctrine:
            return Response({
                "doctrine": serializers.DoctrineSerializer(doctrine).data,
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Doctrine not found!",
        }, status=status.HTTP_404_NOT_FOUND)


class RecentlyWatchedAPI(APIView):
    '''CBV for getting user's recenty watched messages'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        messages = RecentlyWatched.objects.filter(user=user)
        return Response({
            "messages": serializers.MessageSerializer(messages).data,
        }, status=status.HTTP_200_OK)


class BookmarkMessageAPI(APIView):
    '''This CBV is used to bookmark a message'''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        results = []
        bookmarks = Bookmark.objects.filter(user=user).order_by('-created_at')
        for bookmark in bookmarks:
            results.append(
                {
                    'bookmark_id': bookmark.id,  # type: ignore
                    'bookmark_created_at': bookmark.created_at,
                    'message_id': bookmark.message.id,  # type: ignore
                    'message_title': bookmark.message.title,
                    'message_media': bookmark.message.media.url,
                    'message_media_type': bookmark.message.media_type.upper(),
                    'message_category': bookmark.message.category.name.upper(),
                    'message_preacher': bookmark.message.preacher.title.upper() + '. ' + bookmark.message.preacher.name.upper(),
                    'message_created_at': bookmark.created_at,
                }
            )
        return Response({
            "bookmarks": results,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        message_id = request.data.get('message_id')
        message = Message.objects.filter(id=message_id).first()
        if message:
            Bookmark.objects.create(user=user, message=message)
            return Response({
                "message": "Message bookmarked successfully!",
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid message!",
        }, status=status.HTTP_400_BAD_REQUEST)


class RemoveBookmarkAPI(APIView):
    '''This CBV is used to remove a bookmark'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        bookmark_id = request.data.get('bookmark_id')
        bookmark = Bookmark.objects.filter(user=user, id=bookmark_id).first()  # noqa
        if bookmark:
            bookmark.delete()
            return Response({
                "message": "Message Removed From Bookmark!",
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid bookmark!",
        }, status=status.HTTP_400_BAD_REQUEST)


class GeneralNotesListAPI(APIView):
    '''This CBV is used to get all general notes'''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        notes = GeneralNote.objects.filter(user=user).order_by('-created_at')
        return Response({
            "notes": GeneralNoteSerializer(notes, many=True).data,
        }, status=status.HTTP_200_OK)


class CreateUpdateGeneralNoteAPI(APIView):
    '''This CBV is used to add a general note'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        note = request.data.get('note')
        title = request.data.get('title')
        GeneralNote.objects.create(user=user, note=note, title=title)  # noqa
        return Response({
            "message": "Note added successfully!",
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        note_id = request.data.get('note_id')
        note = GeneralNote.objects.filter(
            user=user, id=note_id).first()
        if not note:
            return Response({
                "message": "Invalid note!",
            }, status=status.HTTP_400_BAD_REQUEST)
        note.note = request.data.get('note')
        note.title = request.data.get('title')
        note.save()
        return Response({
            "message": "Note Updated successfully!",
        }, status=status.HTTP_200_OK)


class DeleteGeneralNoteAPI(APIView):
    '''This CBV is used to delete general note'''
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        note_id = request.data.get('note_id')
        note = GeneralNote.objects.filter(user=user, id=note_id).first()  # noqa
        if note:
            note.delete()
            return Response({
                "message": "Note Deleted Successfully!",
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid Note!",
        }, status=status.HTTP_400_BAD_REQUEST)


class GalleryAPI(APIView):
    '''This CBV is used to get all gallery images'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        images = Gallery.objects.all().order_by('-created_at')
        return Response({
            "images": GallerySerializer(images, many=True).data,
        }, status=status.HTTP_200_OK)


class MakeDonationAPI(APIView):
    # this is used to make a donation
    def generate_transaction_id(self):
        return int(round(time.time() * 10000))

    def post(self, request, *args, **kwargs):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = self.generate_transaction_id()
            data = {
                'transaction_id': transaction_id,
                'mobile_number': serializer['mobile_number'].value,
                'amount': serializer['amount'].value,
                'wallet_id': settings.PAYHUB_WALLET_ID,
                'network_code': serializer['network'].value,
            }
            # initiate payment
            receive_payment(data)
            transaction_is_successful = False
            # wait for 30 seconds for payment to be completed
            for i in range(6):
                time.sleep(5)
                transaction_status = get_transaction_status(transaction_id)  # noqa
                print(transaction_status)
                if transaction_status['success'] == True:
                    transaction_is_successful = True
                    print('the transaction was successful')
                    break

            transaction = {
                'transaction_id': transaction_id,
                'amount': serializer['amount'].value,
                'mobile_number': serializer['mobile_number'].value,
                'network': serializer['network'].value,
                'status_code': transaction_status['status_code'],
                'status_message': transaction_status['message'],
            }
            print("Saving Transaction")
            transaction = Donation.objects.create(**transaction)
            print('Transaction Saved')
            serializer = DonationSerializer(transaction, many=False)
            if transaction_is_successful:
                return Response({
                    "status": "success",
                    "transaction": serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "pending",
                    "transaction": serializer.data,
                }, status=status.HTTP_201_CREATED)
        # if transaction data is not valid
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
