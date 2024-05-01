from django.shortcuts import render

from .forms import TicketForm
from .models import Ticket


def default(request):
    print('ok buddy')
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

# Create your views here.
