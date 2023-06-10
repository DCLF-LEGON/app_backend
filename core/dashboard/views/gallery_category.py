from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly
from dashboard.forms import GalleryCategoryForm
from dashboard.models import Gallery, GalleryCategory


class GalleryCategoryView(View):
    '''CBV for showing gallery page'''
    template = 'dashboard/gallery_category.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        categories = GalleryCategory.objects.all()
        context = {
            'categories': categories,
            'total_gallery_category': categories.count()
        }
        return render(request, self.template, context)


class CreateGalleryCategoryView(View):
    '''CBV for adding images to the gallery'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:gallery_category')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        form = GalleryCategoryForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery Category Added Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for k, v in form.errors:
                messages.error(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteGalleryCategoryView(View):
    '''CBV for deleting gallery category'''''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:gallery_category')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        category = GalleryCategory.objects.filter(id=category_id).first()
        if category is not None:
            category.delete()
            messages.success(request, 'Gallery Category Deleted Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request, 'Gallery Category Not Found')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
