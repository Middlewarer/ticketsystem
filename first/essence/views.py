from django.shortcuts import render

def default(request):
    print('ok buddy')
    return render(request, 'essence/base.html')

# Create your views here.
