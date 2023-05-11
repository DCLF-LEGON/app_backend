from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin
from dashboard.models import YoutubeVideo, MessageCategory, Preacher
import requests


class YoutubeVideosView(View):
    '''CBV for viewing youtube videos list page'''

    template = 'dashboard/youtube_messages.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        youtube_video = YoutubeVideo.objects.all().order_by('-published_at')
        context = {
            'youtube_video': youtube_video,
            'total_messages': youtube_video.count(),
        }
        return render(request, self.template, context)


class YoutubeVideoDetailView(View):
    '''CBV for viewing youtube video detail page'''

    template = 'dashboard/details/details_yt_video.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        video_id = request.GET.get('video_id') or None
        video = YoutubeVideo.objects.filter(video_id=video_id).first()
        categories = MessageCategory.objects.all().order_by('name')
        preachers = Preacher.objects.all().order_by('name')
        context = {
            'video': video,
            'categories': categories,
            'preachers': preachers,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        video_id = request.POST.get('video_id') or None
        category_id = request.POST.get('category_id') or None
        preacher_id = request.POST.get('preacher_id') or None
        video = YoutubeVideo.objects.filter(video_id=video_id).first()
        preacher = Preacher.objects.filter(id=preacher_id).first()
        category = MessageCategory.objects.filter(id=category_id).first()
        if video:
            video.category = category
            video.preacher = preacher
            video.save()
            messages.success(request, 'Video Updated Successfully')
        else:
            messages.info(request, 'Something Went Wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FetchYoutubeVideosView(View):
    '''CBV for fetching videos from youtube api and saving into the db'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        try:
            response = requests.get('http://127.0.0.1:8000/api/fetch-youtube-videos/')  # noqa
            if response.status_code == 200:
                res_message = response.json().get('message')
                total_videos = response.json().get('total_videos')
                messages.success(request, f"{res_message} | {total_videos} Videos Added")  # noqa
            else:
                messages.info(request, 'Something Went Wrong')
        except Exception as e:
            messages.info(request, str(e))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UpdateYoutubeVideoView(View):
    '''CBV for updating the info of a youtube video'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to youtube videos list if request is get'''
        return redirect('dashboard:youtube_videos')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        video_id = request.post.get('video_id') or None
        category_id = request.post.get('category_id') or None
        preacher_id = request.post.get('preacher_id') or None
        video = YoutubeVideo.objects.filter(video_id=video_id).first()
        category = MessageCategory.objects.filter(id=category_id).first()
        preacher = Preacher.objects.filter(id=preacher_id).first()
        if video:
            video.category = category
            video.preacher = preacher
            video.save()
            messages.success(request, 'Video Updated Successfully')
        else:
            messages.info(request, 'Video Not Found')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchYoutubeVideoView(View):
    '''CBV for searching youtube videos saved in the db'''

    template = 'dashboard/youtube_messages.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        youtube_video = YoutubeVideo.objects.filter(
            Q(title__icontains=query) |
            Q(video_id__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-published_at')
        context = {
            'youtube_video': youtube_video,
            'total_messages': youtube_video.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteYoutubeVideoView(View):
    '''CBV for deleting a youtube video from the db'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to youtube videos list if request is get'''
        return redirect('dashboard:youtube_videos')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        video_id = request.POST.get('video_id') or None
        if video_id:
            YoutubeVideo.objects.filter(video_id=video_id).delete()
            messages.success(request, 'Video Deleted Successfully')
        else:
            messages.info(request, 'Video ID is Required')
        return redirect('dashboard:youtube_videos')
