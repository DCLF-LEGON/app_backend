from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from core.utils.constants import UserRoles
from accounts.models import User
from dashboard.forms import UserForm


class UsersListView(View):
    '''CBV for the users page'''
    template = 'dashboard/users.html'

    def get(self, request):
        query = request.GET.get('q')
        if query == UserRoles.app_user.value:
            # filter for only app users
            users = User.objects.filter(is_appuser=True).order_by('-date_joined')  # noqa
        elif query == UserRoles.administrator.value:
            # filter for only admins (staff, superuser)
            users = User.objects.filter(is_staff=True).order_by('-date_joined')  # noqa
        else:
            users = User.objects.all().order_by('-date_joined')
        context = {
            "users": users,
            "total_users": users.count(),
        }
        return render(request, self.template, context)


class CreateUpdateUserView(View):
    '''CBV for creating and updating users'''
    template = 'dashboard/form-renderers/create_update_user.html'

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        # new user
        if user_id:
            user = User.objects.filter(id=user_id).first()
        else:
            user = None
        context = {
            'head': 'Create',
            'user': user,
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        # new user
        if not user_id:
            form = UserForm(request.POST, request.FILES or None)  # noqa
            if form.is_valid():
                form.save()
                messages.success(request, 'User created successfully')
                return redirect('dashboard:users')
            else:
                for k, v in form.errors.items():
                    messages.info(request, f'{k}: {v}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # update user
        form = UserForm(request.POST, request.FILES or None, instance=user)  # noqa
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('dashboard:users')
        else:
            print(form.errors)
            for k, v in form.errors.items():
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserDetailsView(View):
    '''CBV for user details'''
    template = 'dashboard/details/details_user.html'

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        context = {
            'user': user,
        }
        return render(request, self.template, context)


class SearchUsersView(View):
    '''CBV for searching users'''
    template = 'dashboard/users.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(fullname__icontains=query) |
            Q(phone__icontains=query)
        ).order_by('-date_joined')
        context = {
            'users': users,
            'total_users': users.count(),
        }
        return render(request, self.template, context)


class DeleteUserView(View):
    '''CBV for deleting users'''

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
            messages.success(request, 'User deleted successfully')
        else:
            messages.info(request, 'Error deleting user')
        return redirect('dashboard:users')
