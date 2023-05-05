from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, redirect, render
from django.views import View

# from auth_remember import remember_user


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = True if request.POST.get('remember') == '1' else False
        user = authenticate(request, email=email, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            # if remember:
            #     remember_user(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
