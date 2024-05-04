

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import TicketForm
from .models import Ticket

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='login'), name='dispatch')
class DefaultView(TemplateView, LoginRequiredMixin):
    template_name = 'essence/base.html'


class TicketCreateView(CreateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    template_name = 'essence/cr_ticket.html'
    success_url = reverse_lazy('main:create')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TicketListView(ListView, LoginRequiredMixin):
    template_name = 'essence/ticket_list.html'
    model = Ticket
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.all()


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