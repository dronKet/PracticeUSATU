from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserCreationForm
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserCreationForm()
        if request.method == "POST":
            form = CreateUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account creation successfullys')
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR Password is invalid')
        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
