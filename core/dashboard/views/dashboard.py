from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User
from core.utils.decorators import MustLogin
from core.utils.util_functions import get_api_wallet_balance
from dashboard.models import YoutubeVideo


class DashboardView(View):
    '''CBV for rendering the dashboard page'''

    template = 'dashboard/dashboard.html'

    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        # top five most likes videos
        top_videos = YoutubeVideo.objects.order_by('-likes')[:5]
        context = {
            'balance': get_api_wallet_balance(),
            'users': User.objects.count(),
            'staff_members': User.objects.filter(is_staff=True),
            'top_videos': top_videos,
        }
        messages.info(request, f'Welcome, {user}')
        return render(request, self.template, context)
