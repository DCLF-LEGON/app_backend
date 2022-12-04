from django.shortcuts import render
from django.views import View

from django.utils.decorators import method_decorator
from core.utils.decorators import AdminOnly, MustLogin


class NotificationsListView(View):
    '''CBV for listing notifications'''
    template = 'dashboard/notifications.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
