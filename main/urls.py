from django.urls import path, include
from django.contrib import admin
from . import views








urlpatterns = [
    
    path('test_view', views.test_view, name='test_view'),
    
    path('practice_completed', views.practice_completed, name='practice_completed'),
    path('level', views.level, name='level'),
    path('section', views.section, name='section'),
    path('study', views.study, name='study'),
    path('practice', views.practice, name='practice'),
    path('word_practice', views.word_practice, name='word_practice'),
    path('word_practice_completed', views.word_practice_completed, name='word_practice_completed'),
    path('kanji', views.kanji, name='kanji'),
    path('word', views.word, name='word'),
    path('pronunciations', views.pronunciations, name='pronunciations'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('', views.home, name='home'),
]