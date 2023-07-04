from django.shortcuts import render
from django.views import View


class HomePageView(View):
    '''This view renders the homepage of the website.'''

    template = 'website/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)


class ContactUsView(View):
    '''This view renders the contact us page'''

    template = 'website/contact.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
