from django.urls import path, include
from django.contrib import admin
from . import views








urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('', views.home, name='home'),
]