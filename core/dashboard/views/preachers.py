from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views import View
from django.contrib import messages

from dashboard.forms import PreacherForm
from dashboard.models import Preacher

from django.utils.decorators import method_decorator
from core.utils.decorators import AdminOnly, MustLogin


class PreachersListView(View):
    '''CBV for preachers list page'''

    template = 'dashboard/preachers.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        preachers = Preacher.objects.all().order_by('-created_at')
        context = {
            'preachers': preachers,
            'total_preachers': preachers.count(),
        }
        return render(request, self.template, context)


class CreatePreacherView(View):
    '''CBV for create preacher page'''

    template = 'dashboard/form-renderers/create_update_preacher.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        preacher_id = request.GET.get('preacher_id') or None
        preacher = Preacher.objects.filter(id=preacher_id).first()
        context = {
            "head": "Create",
            'preacher': preacher,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        preacher_id = request.POST.get('preacher_id') or None
        preacher = Preacher.objects.filter(id=preacher_id).first()
        form = PreacherForm(request.POST, request.FILES or None, instance=preacher)  # noqa
        if form.is_valid():
            form.save()
            if preacher_id:
                messages.info(request, 'Preacher updated successfully')
            else:
                messages.info(request, 'Preacher created successfully')
            return redirect('dashboard:preachers')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PreacherDetailsView(View):
    '''CBV for preacher details page'''

    template = 'dashboard/details/details_preacher.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        preacher_id = request.GET.get('preacher_id')
        preacher = Preacher.objects.filter(id=preacher_id).first()
        context = {
            'preacher': preacher,
        }
        return render(request, self.template, context)


class SearchPreacherView(View):
    '''CBV for searching preachers'''

    template = 'dashboard/preachers.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        preachers = Preacher.objects.filter(
            Q(name__icontains=query) |
            Q(position__icontains=query) |
            Q(title__icontains=query)
        ).order_by('-created_at')
        context = {
            'preachers': preachers,
            'total_preachers': preachers.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeletePreacherView(View):
    '''CBV for deleting a preacher'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to preachers list is request is get'''
        return redirect('dashboard:preachers')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        preacher_id = request.POST.get('preacher_id') or None
        if preacher_id:
            Preacher.objects.filter(id=preacher_id).delete()
            messages.success(request, 'Preacher deleted successfully')
        return redirect('dashboard:preachers')
