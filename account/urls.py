from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('logout/', 
        auth_views.LogoutView.as_view(
        template_name='registration/log_out.html'), name='logout'),
    path('', views.dashboard, name='dashboard'),
]