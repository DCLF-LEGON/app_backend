from django.shortcuts import render
from django.views import View


class NotificationsListView(View):
    '''CBV for listing notifications'''
    template = 'dashboard/notifications.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
