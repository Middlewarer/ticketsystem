
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import TicketForm, UserProfileForm
from .models import Ticket

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DefaultView(TemplateView, LoginRequiredMixin):
    template_name = 'main/base.html'


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'main/profile.html'
    model = User
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        context['seeker'] = Ticket.objects.filter(seeker=current_user).order_by('-id')
        context['agent'] = Ticket.objects.filter(agent=current_user).order_by('-id')

        return context


def user_tickets_api(request):
    current_user = request.user
    seeker_tickets = Ticket.objects.filter(seeker=current_user).order_by('-id')
    agent_tickets = Ticket.objects.filter(agent=current_user).order_by('-id')

    data_of_tickets = list()
    for item in seeker_tickets:
        data_of_tickets.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "seeker": item.seeker if item.seeker else "-",
            "agent": item.agent if item.agent else "-",
            "status": item.status,
            "priority": item.priority,
            "resolved": item.resolved
        })

    return JsonResponse({"data": data_of_tickets})


class TicketCreateView(CreateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    template_name = 'main/cr_ticket.html'
    success_url = reverse_lazy('main:create')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TicketListView(ListView, LoginRequiredMixin):
    model = Ticket
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.all()


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'main/edit.html'
    success_url = reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        return self.request.user


def table_api(request):
    list_ticket = list()
    ticket = Ticket.objects.all()
    for item in ticket:
        data = {"id": item.id,
                "title": item.title,
                "description": item.description,
                "seeker": item.seeker if item.seeker else "-",
                "agent": item.agent if item.agent else "-",
                "status": item.status,
                "priority": item.priority,
                "resolved": item.resolved}

        list_ticket.append(data)

    return JsonResponse({"data": list_ticket})