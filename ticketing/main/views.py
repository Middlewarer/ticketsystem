from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import TicketForm, UserProfileForm
from .models import Ticket

from django.db.models import Q


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

    data_of_tickets = list()
    for item in seeker_tickets:
        seeker_id = item.seeker.id if item.seeker else '-'
        agent_id = item.agent.id if item.agent else '-'
        data_of_tickets.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "seeker": seeker_id,
            "agent": agent_id,
            "status": item.status,
            "priority": item.priority,
            "resolved": item.resolved
        })

    return JsonResponse({"data": data_of_tickets})


def user_new_tickets_api(request):
    current_user = request.user
    agent_tickets = Ticket.objects.filter(agent=current_user).order_by('-id')

    data_of_tickets = list()
    for item in agent_tickets:
        seeker_id = item.seeker.id if item.seeker else '-'
        agent_id = item.agent.id if item.agent else '-'
        data_of_tickets.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "seeker": seeker_id,
            "agent": agent_id,
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
        ticket = form.save(commit=False)
        ticket.seeker = self.request.user
        ticket.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TicketListView(ListView, LoginRequiredMixin):
    model = Ticket
    context_object_name = 'tickets'

    def get_queryset(self):
        tickets_with_agent = Ticket.objects.filter(agent__isnull=False)
        return tickets_with_agent


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'main/edit.html'
    success_url = '/done/profile'

    def get_object(self, queryset=None):
        return self.request.user


def table_api(request):
    list_ticket = list()
    tickets = Ticket.objects.all()

    for item in tickets:
        seeker_id = item.seeker.id if item.seeker else None
        seeker_username = item.seeker.username if item.seeker else None

        agent_id = item.agent.id if item.agent else None
        agent_username = item.agent.username if item.agent else None

        data = {"id": item.id,
                "title": item.title,
                "description": item.description,

                "seeker": {'id': seeker_id,
                           'username': seeker_username},

                "agent": {
                        "id": agent_id,
                        "username": agent_username},

                "status": item.status,
                "priority": item.priority,
                "resolved": item.resolved}

        list_ticket.append(data)

    return JsonResponse({"data": list_ticket})


class TicketDetailView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'main/tc_detail.html'
    context_object_name = 'ticket'
    success_url = 'done/profile'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'become_agent' in request.POST:
            self.object.agent = request.user
            self.object.save()

            return redirect('main:profile')

        return super().post(request, *args, **kwargs)