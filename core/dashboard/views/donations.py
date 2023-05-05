import csv
import datetime

from django.db.models import Q
from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin
from dashboard.models import Donation


class DonationsListView(View):
    '''CBV for donations list page'''

    template = 'dashboard/donations.html'

    @method_decorator(MustLogin)
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

    @method_decorator(MustLogin)
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


class DownloadDonationsAsCSV(View):
    '''CBV for downloading donations as CSV'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="donations.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Transaction ID',
            'Amount',
            'Network',
            'Mobile Number',
            'Status Code',
            'Status Message',
            'Created At',
        ])
        for donation in donations:
            writer.writerow([
                donation.transaction_id,
                donation.amount,
                donation.network,
                donation.mobile_number,
                donation.status_code,
                donation.status_message,
                donation.created_at,
            ])
        return response


class DownloadDonationsAsExcel(View):
    '''CBV for downloading donations as Excel'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="donations.xls"'
        writer = csv.writer(response)
        writer.writerow([
            'Transaction ID',
            'Amount',
            'Network',
            'Mobile Number',
            'Status Code',
            'Status Message',
            'Created At',
        ])
        for donation in donations:
            writer.writerow([
                donation.transaction_id,
                donation.amount,
                donation.network,
                donation.mobile_number,
                donation.status_code,
                donation.status_message,
                donation.created_at,
            ])
        return response


class DownloadDonationsAsPDF(View):
    '''CBV for downloading donations as PDF'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="donations.pdf"'
        writer = csv.writer(response)
        writer.writerow([
            'Transaction ID',
            'Amount',
            'Network',
            'Mobile Number',
            'Status Code',
            'Status Message',
            'Created At',
        ])
        for donation in donations:
            writer.writerow([
                donation.transaction_id,
                donation.amount,
                donation.network,
                donation.mobile_number,
                donation.status_code,
                donation.status_message,
                donation.created_at,
            ])
        return response
