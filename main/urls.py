from django.conf.urls import url, include
from django.contrib import admin
from . import views








urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^practice_completed$', views.practice_completed, name='practice_completed'),
    url(r'^level$', views.level, name='level'),
    url(r'^section$', views.section, name='section'),
    url(r'^study$', views.study, name='study'),
    url(r'^practice$', views.practice, name='practice'),
    url(r'^word_practice$', views.word_practice, name='word_practice'),
    url(r'^word_practice_completed$', views.word_practice_completed, name='word_practice_completed'),
    url(r'^kanji$', views.kanji, name='kanji'),
    url(r'^word$', views.word, name='word'),
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
]