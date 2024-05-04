from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [

    path('default/', views.DefaultView.as_view(), name='default'),
    path('create/', views.TicketCreateView.as_view(), name='create'),
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('api/', views.table_api, name='api'),

]