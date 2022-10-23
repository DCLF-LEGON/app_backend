from django.db.models import Q
from django.shortcuts import render
from django.views import View

from dashboard.models import Donation

import datetime

# from django.utils.timzone import now


class DonationsListView(View):
    '''CBV for donations list page'''

    template = 'dashboard/donations.html'

    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all().order_by('-created_at')
        # today = now().date()
        today = datetime.date.today()
        donations_today = Donation.objects.filter(created_at__date=today).count()  # noqa
        context = {
            'donations': donations,
            'donations_today': donations_today,
            'total_donations': donations.count(),
        }
        return render(request, self.template, context)


class SearchDonationView(View):
    '''CBV for searching donations'''

    template = 'dashboard/donations.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        donations = Donation.objects.filter(
            Q(transaction_id__icontains=query) |
            Q(amount__icontains=query) |
            Q(network__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(status_code__icontains=query) |
            Q(status_message__icontains=query)
        ).order_by('-created_at')
        context = {
            'donations': donations,
            'total_donations': donations.count(),
            'search': True,
        }
        return render(request, self.template, context)
