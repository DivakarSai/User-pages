from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='user_login'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile')
]