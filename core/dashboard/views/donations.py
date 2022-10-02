from django.shortcuts import render
from django.views import View


class DonationsListView(View):
    '''CBV for donations list page'''

    template = 'dashboard/donations.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)