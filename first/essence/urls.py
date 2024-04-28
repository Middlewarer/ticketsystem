from django.urls import path
from . import views

app_name = 'essence'

urlpatterns = [
    path('default/', views.default, name='default'),
]