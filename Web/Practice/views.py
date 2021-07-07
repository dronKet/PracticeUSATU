from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    count = User.objects.count()
    return render(request, 'pages/home.html', {'count': count})
