from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from dashboard.forms import MessageCategoryForm

from dashboard.models import MessageCategory

from django.utils.decorators import method_decorator
from core.utils.decorators import AdminOnly, MustLogin


class CategoriesListView(View):
    '''CBV for messsages categories list page'''

    template = 'dashboard/categories.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        categories = MessageCategory.objects.all().order_by('-created_at')
        context = {
            'categories': categories,
            'total_categories': categories.count(),
        }
        return render(request, self.template, context)


class CreateUpdateCategoryView(View):
    '''CBV for create/update message category'''

    template = 'dashboard/form-renderers/create_update_category.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id') or None
        category = MessageCategory.objects.filter(id=category_id).first()
        if category:
            head = "Update"
        else:
            head = "Create"
        context = {
            "head": head,
            'category': category,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id') or None
        category = MessageCategory.objects.filter(id=category_id).first()
        form = MessageCategoryForm(request.POST, request.FILES, instance=category)  # noqa
        if form.is_valid():
            form.save()
            if category_id:
                messages.info(request, 'Message Category updated successfully')
            else:
                messages.info(request, 'Message Category created successfully')
            return redirect('dashboard:categories')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchCategoryView(View):
    '''CBV for searching messages category'''

    template = 'dashboard/categories.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        categories = MessageCategory.objects.filter(
            Q(name__icontains=query)
        ).order_by('-created_at')
        context = {
            'categories': categories,
            'total_categories': categories.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteCategoryView(View):
    '''CBV for deleting a message category'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to messages categories list if request is get'''
        return redirect('dashboard:categories')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id') or None
        if category_id:
            MessageCategory.objects.filter(id=category_id).delete()
            messages.success(request, 'Message Category deleted successfully')
        return redirect('dashboard:categories')
