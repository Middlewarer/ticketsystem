from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [

    path('', views.login_view, name='login'),
    path('signup/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

]