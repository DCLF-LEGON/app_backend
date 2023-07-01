from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import MustLogin
from dashboard.forms import LiveStreamForm
from dashboard.models import LiveStream


class LiveStreamListView(View):
    '''CBV for LiveStream list page'''

    template = 'dashboard/live_stream.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        livestreams = LiveStream.objects.all().order_by('-created_at')
        context = {
            'livestreams': livestreams,
            'total_streams': livestreams.count(),
        }
        return render(request, self.template, context)


class CreateUpdateLiveStreamView(View):
    '''CBV for create/update LiveStream'''

    template = 'dashboard/form-renderers/create_update_livestream.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        stream_id = request.GET.get('stream_id') or None
        stream = LiveStream.objects.filter(id=stream_id).first()
        if stream:
            head = "Update"
        else:
            head = "Create"
        context = {
            "head": head,
            'stream': stream,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        stream_id = request.POST.get('stream_id') or None
        stream = LiveStream.objects.filter(id=stream_id).first()
        form = LiveStreamForm(request.POST, instance=stream)  # noqa
        if form.is_valid():
            stream_item = form.save()
            stream_item.video_id = stream_item.url.split("=")[1]
            stream_item.save()
            if stream:
                messages.info(request, 'Stream Updated Successfully')
            else:
                messages.info(request, 'Stream Created Successfully')
            return redirect('dashboard:streams')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchLiveStreamView(View):
    '''CBV for searching LiveStream messages'''

    template = 'dashboard/live_stream.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        livestreams = LiveStream.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(preacher__icontains=query) |
            Q(url__icontains=query)
        ).order_by('-created_at')
        context = {
            'livestreams': livestreams,
            'total_streams': livestreams.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteLiveStreamView(View):
    '''CBV for deleting a a live stream'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to messages categories list if request is get'''
        return redirect('dashboard:streams')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        stream_id = request.POST.get('stream_id') or None
        stream = LiveStream.objects.filter(id=stream_id).first()
        if stream:
            stream.delete()
            messages.success(request, 'Live Stream Deleted Successfully')
            return redirect('dashboard:streams')
        else:
            messages.error(request, 'Live Stream Not Found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
