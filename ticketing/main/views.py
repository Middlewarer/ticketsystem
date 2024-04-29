from django.shortcuts import render

def default(request):
    print('ok buddy')
    return render(request, 'main/base.html')

# Create your views here.
