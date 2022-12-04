
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.views import View

from core.utils.decorators import AdminOnly, MustLogin


class ProfileView(View):
    '''CBV for profile page'''

    template = 'dashboard/profile.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template, context)


class ProfileUpdateView(View):
    '''CBV for profile update page'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:profile')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        profile_pic = request.FILES.get('profile_pic') or None
        profile_cover = request.FILES.get('profile_cover') or None
        email = request.POST.get('email') or None
        user = request.user
        user.fullname = request.POST.get('fullname')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')
        if email:
            user.email = email
        if profile_pic:
            user.profile_pic = profile_pic
        if profile_cover:
            user.profile_cover = profile_cover
        user.save()
        messages.success(request, 'Profile Updated successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PasswordResetView(View):
    '''CBV for password reset page'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:profile')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = request.user
            user.set_password(password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'Password does not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
