from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin
from dashboard.models import YoutubeVideo


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
        ).order_by('-created_at')
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
