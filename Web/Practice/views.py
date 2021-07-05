from django.shortcuts import render
from django.contrib.auth.models import User


def home(request):
    count = User.objects.count()
    return render(request, 'pages/home.html', {'count': count})


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')
