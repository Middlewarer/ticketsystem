from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


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

