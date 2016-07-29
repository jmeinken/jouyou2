from django.conf.urls import url, include
from django.contrib import admin
from . import views








urlpatterns = [
    # commented out urls will immediately start doing something drastic
    # url(r'^$', views.dashboard, name='dashboard'),
    url(r'^import_kanji_data', views.import_kanji_data, name='import_kanji_data'),
    url(r'^import_kanji_component_data', views.import_kanji_component_data, name='import_kanji_component_data'),
    url(r'^hybrid_sort', views.hybrid_sort, name='hybrid_sort'), 
    url(r'^import_words', views.import_words, name='import_words'), 
    url(r'^populate_level', views.populate_level, name='populate_level'), 
    url(r'^populate_section', views.populate_section, name='populate_section'), 
]