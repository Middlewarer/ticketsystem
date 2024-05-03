from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

from django.contrib.auth.decorators import login_required


@login_required(login_url='authentication:login')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        print('okok')
        if form.is_valid():
            print('hohoho')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('ok buddy')
                return redirect('main:default')
    else:
        form = LoginForm()

    return render(request, 'authentication/auth.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:default')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('authentication:login')