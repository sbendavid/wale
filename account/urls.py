from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='log_out'),
    path('signup/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard')
]