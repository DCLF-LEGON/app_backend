from django.shortcuts import render
from django.views import View


class PreachersListView(View):
    '''CBV for preachers list page'''

    template = 'dashboard/preachers.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
