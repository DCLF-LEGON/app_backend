from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # user = authenticate(request, username=email, password=password)
        # if user is not None and user.is_staff:
        #     # redirect to otp page
        #     # do the redirection here
        #     login(request, user)
        #     return redirect('dashboard')
        # else:
        #     messages.error(request, 'Invalid credentials')
        #     return redirect('accounts:login')
        # NOTE: This is just a temporary code to test the dashboard
        return redirect('dashboard:dashboard')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
