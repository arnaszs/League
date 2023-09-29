from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'html/home.html'


class CustomLoginView(LoginView):
    template_name = 'html/login.html'


def home_view(request):
    return render(request, 'html/home.html')


def login_view(request):
    return render(request, 'html/login.html')
