from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from dictionary.models import LearnableConcept, Word
from .models import ConceptUser



def get_concept_user_for_concept(oConcept, oUser):
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=oUser).first()
    return oConceptUser()

def unlock_words(oConceptUser):
    oUser = oConceptUser.user
    # concept must be a kanji or this doesn't make sense
    if not oConceptUser.concept.type == 'kanji':
        raise ValueError('Expecting a kanji, got something else.')
    # get all words that contain this kanji and have not already been unlocked
    qWord = oConceptUser.concept.kanji.word_set.all()
    # qWord = qWord.filter(concept__conceptuser__user=oUser)
    # for each word, check if all kanji are completed
    for oWord in qWord:
        if get_concept_user_for_concept(oWord.concept, oUser):
            continue
        word_complete = True
        for oKanji in oWord.kanji_set.all():
            if not get_concept_user_for_concept(oKanji.concept, oUser):
                word_complete = False
        if word_complete:
            oConceptUser = ConceptUser(concept=oWord.concept, user=oUser)
            oConceptUser.save()
            
            
    # if yes, unlock word

def quiz_submit_answer(request):
    concept_user_id = request.GET.get('concept_user_id')
    correct_str = request.GET.get('correct')
    correct = True if correct_str == 'true' else False
    print(correct, type(correct))
    oConceptUser = get_object_or_404(ConceptUser, pk=concept_user_id)
    context = {}
    if correct and oConceptUser.level == 9:
        # time to unlock words
        pass
    if correct and oConceptUser.level < 10:
        context['level_change'] = '+1'
        oConceptUser.level += 1
    if not correct and oConceptUser.level < 10 and oConceptUser.level > 0:
        context['level_change'] = '-1'
        oConceptUser.level -= 1
    oConceptUser.save()    # this also marks it as modified
    context['oConceptUser'] = oConceptUser
    response = {}
    response['html'] = render_to_string('study/snippets/quiz_progress.html', context, request=request)
    return JsonResponse(response)
        

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
    
    
def practice_get_answer(request):
    pass