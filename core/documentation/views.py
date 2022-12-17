from django.shortcuts import render
from django.views import View


class DocumentationView(View):
    '''This view renders the documentation page.'''

    template = 'documentation/documentation.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
