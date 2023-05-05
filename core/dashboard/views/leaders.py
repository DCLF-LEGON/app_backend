from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin
from dashboard.forms import LeaderForm
from dashboard.models import Leader


class LeadersListView(View):
    '''CBV for leaders list page'''

    template = 'dashboard/leaders.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        leaders = Leader.objects.all().order_by('-created_at')
        context = {
            'leaders': leaders,
            'total_leaders': leaders.count(),
        }
        return render(request, self.template, context)


class CreateLeaderView(View):
    '''CBV for create leader page'''

    template = 'dashboard/form-renderers/create_update_leader.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        leader_id = request.GET.get('leader_id') or None
        leader = Leader.objects.filter(id=leader_id).first()
        context = {
            "head": "Create",
            'leader': leader,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        leader_id = request.POST.get('leader_id') or None
        leader = Leader.objects.filter(id=leader_id).first()
        form = LeaderForm(request.POST, request.FILES or None, instance=leader)  # noqa
        if form.is_valid():
            form.save()
            if leader_id:
                messages.info(request, 'Leader updated successfully')
            else:
                messages.info(request, 'Leader created successfully')
            return redirect('dashboard:leaders')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LeaderDetailsView(View):
    '''CBV for leader details page'''

    template = 'dashboard/details/details_leader.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        leader_id = request.GET.get('leader_id')
        leader = Leader.objects.filter(id=leader_id).first()
        context = {
            'leader': leader,
        }
        return render(request, self.template, context)


class SearchLeaderView(View):
    '''CBV for searching leaders'''

    template = 'dashboard/leaders.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        leaders = Leader.objects.filter(
            Q(name__icontains=query) |
            Q(position__icontains=query) |
            Q(title__icontains=query)
        ).order_by('-created_at')
        context = {
            'leaders': leaders,
            'total_leaders': leaders.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteLeaderView(View):
    '''CBV for deleting a leader'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to leaders list if request is get'''
        return redirect('dashboard:leaders')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        leader_id = request.POST.get('leader_id') or None
        if leader_id:
            Leader.objects.filter(id=leader_id).delete()
            messages.success(request, 'Leader deleted successfully')
        return redirect('dashboard:leaders')
