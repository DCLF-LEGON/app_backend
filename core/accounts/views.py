from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>Login page</h1>')

    # def post(self, request):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         return HttpResponse('Invalid credentials')
