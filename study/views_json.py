from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from dictionary.models import LearnableConcept
from .models import ConceptUser


def lookup_concept_detailed(request, concept_id):

    oConcept = get_object_or_404(LearnableConcept, pk=concept_id)
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=request.user).first()
    
    context = {
        'oConcept' : oConcept,
        'oKanji' : oConcept.kanji,
        'oConceptUser' : oConceptUser,
    }
    
    response = {
        'html' : render_to_string('study/snippets/kanji_details.html', context, request=request)
    }
    return JsonResponse(response)

def lookup_word_detailed(request, concept_id):
    oConcept = get_object_or_404(LearnableConcept, pk=concept_id)