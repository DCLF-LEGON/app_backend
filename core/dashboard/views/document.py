from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.decorators import AdminOnly
from dashboard.forms import ChurchDocumentForm
from dashboard.models import ChurchDocument, GalleryCategory


class ChurchDocumentView(View):
    '''CBV for showing church document page'''
    template = 'dashboard/document.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        document = ChurchDocument.objects.all()
        context = {
            'document': document,
            'total_document': document.count(),
        }
        return render(request, self.template, context)


class AddChurchDocumentView(View):
    '''CBV for adding church document'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:document')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        form = ChurchDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document Added Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for k, v in form.errors:
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteChurchDocumentView(View):
    '''CBV for deleting church document'''

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:document')

    @method_decorator(AdminOnly)
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')
        document = ChurchDocument.objects.filter(id=doc_id).first()
        if document is not None:
            document.delete()
            messages.success(request, 'Document Deleted Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request, 'Document Not Found')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
