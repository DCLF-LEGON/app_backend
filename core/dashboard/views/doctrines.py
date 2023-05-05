from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin
from dashboard.forms import DoctrineForm
from dashboard.models import Doctrine


class DoctrinesListView(View):
    '''CBV for messsages doctrines list page'''

    template = 'dashboard/doctrines.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        doctrines = Doctrine.objects.all().order_by('-created_at')
        context = {
            'doctrines': doctrines,
            'total_doctrines': doctrines.count(),
        }
        return render(request, self.template, context)


class CreateUpdateDoctrineView(View):
    '''CBV for create/update doctrine'''

    template = 'dashboard/form-renderers/create_update_doctrine.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        doctrine_id = request.GET.get('doctrine_id') or None
        doctrine = Doctrine.objects.filter(id=doctrine_id).first()
        if doctrine:
            head = "Update"
        else:
            head = "Create"
        context = {
            "head": head,
            'doctrine': doctrine,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        doctrine_id = request.POST.get('doctrine_id') or None
        doctrine = Doctrine.objects.filter(id=doctrine_id).first()
        form = DoctrineForm(request.POST, instance=doctrine)  # noqa
        if form.is_valid():
            form.save()
            if doctrine_id:
                messages.info(request, 'Doctrine updated successfully')
            else:
                messages.info(request, 'Doctrine created successfully')
            return redirect('dashboard:doctrines')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchDoctrineView(View):
    '''CBV for searching doctrine'''

    template = 'dashboard/doctrines.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        doctrines = Doctrine.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')
        context = {
            'doctrines': doctrines,
            'total_doctrines': doctrines.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DoctrineDetailsView(View):
    '''CBV for doctrine details page'''

    template = 'dashboard/details/details_doctrine.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        doctrine_id = request.GET.get('doctrine_id')
        doctrine = Doctrine.objects.filter(id=doctrine_id).first()
        context = {
            'doctrine': doctrine,
        }
        return render(request, self.template, context)


class DeleteDoctrineView(View):
    '''CBV for deleting a doctrine'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to doctrines list if request is get'''
        return redirect('dashboard:doctrines')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        doctrine_id = request.POST.get('doctrine_id') or None
        if doctrine_id:
            Doctrine.objects.filter(id=doctrine_id).delete()
            messages.success(request, 'Doctrine deleted successfully')
        return redirect('dashboard:doctrines')
