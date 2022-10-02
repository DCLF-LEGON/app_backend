from django.shortcuts import render, HttpResponse
from django.views import View


class CreateUpdateMessageView(View):
    '''CBV for creating and updating messages'''

    def get(self, request, *args, **kwargs):
        return HttpResponse('CreateUpdateMessageView')

    def post(self, request, *args, **kwargs):
        return HttpResponse('CreateUpdateMessageView')

    def put(self, request, *args, **kwargs):
        return HttpResponse('CreateUpdateMessageView')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('CreateUpdateMessageView')
