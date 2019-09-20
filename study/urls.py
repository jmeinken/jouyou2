from django.urls import path, include

from . import views
from . import views_json


urlpatterns = [
   # path('js/graph_functions.js', views.js_graph_functions, name='js_graph_functions'),
   # path('myview2/<int:code>', views.myview2, name='myview2'),
   
   path('api/concept/<int:concept_id>/detailed', views_json.lookup_concept_detailed, name='lookup_concept_detailed'),
   
   path('learn_new_kanji', views.learn_new_kanji, name='learn_new_kanji'),
   path('practice_kanji_in_progress', views.practice_kanji_in_progress, name='practice_kanji_in_progress'),
   path('practice_completed_kanji', views.practice_completed_kanji, name='practice_completed_kanji'),
   
   
   path('', views.home, name='home'),
]