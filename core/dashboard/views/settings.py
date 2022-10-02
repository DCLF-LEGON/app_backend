
from django.shortcuts import render
from django.views import View


class SettingsView(View):
    '''CBV for settings page'''

    template = 'dashboard/settings.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
