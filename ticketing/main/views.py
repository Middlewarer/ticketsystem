from django.shortcuts import render

from .forms import TicketForm


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

# Create your views here.
