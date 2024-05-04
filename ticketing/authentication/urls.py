from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]