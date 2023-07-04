from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from dashboard.forms import ContactUsForm


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

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            print("Contact saved")
            return redirect('website:homepage')
        else:
            print(f"ERRORS: {str(form.errors)}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
