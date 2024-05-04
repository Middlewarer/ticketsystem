from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# -----> ALR Setup


class LoginView(FormView):
    template_name = 'authentication/auth.html'
    form_class = LoginForm
    success_url = 'main:default'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect('main:default')
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RegistrationView(FormView):
    template_name = 'authentication/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main:default')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class LogoutView(RedirectView):
    pattern_name = 'authentication:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return super().dispatch(request, *args, **kwargs)



#-----___----> ALR Endblock
