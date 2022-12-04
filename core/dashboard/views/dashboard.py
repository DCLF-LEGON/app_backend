from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from core.utils.decorators import MustLogin

from core.utils.util_functions import get_api_wallet_balance
from accounts.models import User

from django.utils.decorators import method_decorator


class DashboardView(View):
    '''CBV for rendering the dashboard page'''

    template = 'dashboard/dashboard.html'

    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        context = {
            'balance': get_api_wallet_balance(),
            'users': User.objects.count(),
            'staff_members': User.objects.filter(is_staff=True),
        }
        messages.info(request, f'Welcome, {user}')
        return render(request, self.template, context)
