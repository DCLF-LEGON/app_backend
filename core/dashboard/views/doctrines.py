from django.shortcuts import render
from django.views import View


class DoctrinesListView(View):
    '''CBV for doctrines list page'''

    template = 'dashboard/doctrines.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
