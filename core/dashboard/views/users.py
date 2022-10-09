from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from accounts.models import User
from dashboard.forms import UserForm


class UsersListView(View):
    '''CBV for the users page'''
    template = 'dashboard/users.html'

    def get(self, request):
        users = User.objects.all().order_by('-id')
        context = {
            "users": users,
        }
        return render(request, self.template, context)


class CreateUpdateUserView(View):
    '''CBV for creating and updating users'''
    template = 'dashboard/form-renderers/create_update_user.html'

    def get(self, request, *args, **kwargs):
        context = {
            'head': 'Create',
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        # new user
        if not user_id:
            form = UserForm(request.POST, request.FILES or None)  # noqa
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/users')
            else:
                return HttpResponse('form is not valid')
        # update user
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
            return HttpResponseRedirect("request.META.get('HTTP_REFERER')")
