from django.conf.urls import url, include
from django.contrib import admin
from . import views








urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^levels$', views.levels, name='levels'),
    url(r'^study$', views.study, name='study'),
    url(r'^kanji$', views.kanji, name='kanji'),
    url(r'^word$', views.word, name='word'),
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
]