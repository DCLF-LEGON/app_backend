from django.shortcuts import render
from django.views import View


class LeadersListView(View):
    '''CBV for leaders list page'''

    template = 'dashboard/leaders.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)