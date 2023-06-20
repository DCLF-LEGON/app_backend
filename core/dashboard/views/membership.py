import csv
import datetime

from django.db.models import Q
from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import MembershipInfo

from core.utils.decorators import AdminOnly
from dashboard.models import Donation


class MembershipListView(View):
    '''CBV for Membership list page'''

    template = 'dashboard/membership.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        members = MembershipInfo.objects.all().order_by('-created_at')
        context = {
            'members': members,
            'total_members': members.count(),
        }
        return render(request, self.template, context)


class SearchMembershipView(View):
    '''CBV for searching Membership'''

    template = 'dashboard/membership.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        members = MembershipInfo.objects.filter(
            Q(user__fullname__icontains=query) |
            Q(program__icontains=query) |
            Q(department__icontains=query) |
            Q(hall__icontains=query) |
            Q(level__icontains=query) |
            Q(phone__icontains=query) |
            Q(room__icontains=query)
        ).order_by('-created_at')
        context = {
            'members': members,
            'total_members': members.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DownloadMembershipAsCSV(View):
    '''CBV for downloading Membership as CSV'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        membership = MembershipInfo.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="membership.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Fullname',
            'Level',
            'Program',
            'Department',
            'Hall',
            'Phone',
            'Created At',
        ])
        for member in membership:
            writer.writerow([
                str(member.user.fullname).capitalize(),
                member.level,
                member.program,
                member.department,
                member.hall,
                member.phone,
                member.created_at,
            ])
        return response


class DownloadMembershipAsExcel(View):
    '''CBV for downloading Membership as Excel'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        membership = MembershipInfo.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="membership.xls"'
        writer = csv.writer(response)
        writer.writerow([
            'Fullname',
            'Level',
            'Program',
            'Department',
            'Hall',
            'Phone',
            'Created At',
        ])
        for member in membership:
            writer.writerow([
                str(member.user.fullname).capitalize(),
                member.level,
                member.program,
                member.department,
                member.hall,
                member.phone,
                member.created_at,
            ])
        return response


class DownloadMembershipAsPDF(View):
    '''CBV for downloading donations as PDF'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        membership = MembershipInfo.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="membership.pdf"'
        writer = csv.writer(response)
        writer.writerow([
            'Fullname',
            'Level',
            'Program',
            'Department',
            'Hall',
            'Phone',
            'Created At',
        ])
        for member in membership:
            writer.writerow([
                str(member.user.fullname).capitalize(),
                member.level,
                member.program,
                member.department,
                member.hall,
                member.phone,
                member.created_at,
            ])
        return response
