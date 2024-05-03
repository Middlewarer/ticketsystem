from django.shortcuts import render
from django.http import JsonResponse

from .forms import TicketForm
from .models import Ticket

from django.contrib.auth.decorators import login_required


@login_required(login_url='authentication:login')
def default(request):
    return render(request, 'essence/base.html')

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TicketForm()
    return render(request, 'essence/cr_ticket.html', {"form": form})


def ticket_list_view(request):
    tickets = Ticket.objects.all()
    return render(request, 'essence/ticket_list.html', {"tickets": tickets})


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