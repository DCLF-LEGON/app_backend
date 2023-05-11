from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly
from dashboard.models import Gallery


class GalleryView(View):
    '''CBV for showing gallery page'''
    template = 'dashboard/gallery.html'

    def get(self, request, *args, **kwargs):
        gallery = Gallery.objects.all()
        context = {
            'gallery': gallery,
            'total_gallery': gallery.count()
        }
        return render(request, self.template, context)


class AddImagesView(View):
    '''CBV for adding images to the gallery'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:gallery')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        count = 0
        for image in images:
            try:
                Gallery.objects.create(image=image)
            except Exception as e:
                print(e)
            else:
                count += 1
        if count == 0:
            messages.error(request, 'No Images Added To Gallery')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.success(request, f'{count} Images Added To Gallery Successfully')  # noqa
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteImageView(View):
    '''CBV for deleting gallery image'''''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:gallery')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        image_id = request.POST.get('image_id')
        image = Gallery.objects.filter(id=image_id).first()
        if image is not None:
            image.delete()
            messages.success(request, 'Image Deleted Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request, 'Image Not Found')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
