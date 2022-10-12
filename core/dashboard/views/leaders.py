from django.shortcuts import render
from django.views import View


class LeadersListView(View):
    '''CBV for leaders list page'''

    template = 'dashboard/leaders.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class CreateLeaderView(View):
    '''CBV for create leader page'''

    template = 'dashboard/form-renderers/create_update_leader.html'

    def get(self, request, *args, **kwargs):

        context = {
            "head": "Create"
        }
        return render(request, self.template, context)
