from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [

    path('default/', views.default, name='default'),
    path('create/', views.create_ticket, name='create'),
    path('tickets/', views.ticket_list_view, name='ticket_list'),
    path('api/', views.table_api, name='api'),

]