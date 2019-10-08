from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dictionary.models import LearnableConcept
from . import models
from . import quiz

@login_required
def home(request):
    
    qConceptUserKanji = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_KANJI
    ).order_by('-created')
    
    completed_count = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_KANJI,
        level=10
    ).count()
    
    
    # count kanji studying, kanji completed, words studying, words completed
    # get list of encountered kanji
    
    #get list of encountered words
    context = {
        'current_page' : 'home',
        'qConceptUserKanji' : qConceptUserKanji,
        'completed_count' : completed_count,
    }
    return render(request, 'study/home.html', context)

@login_required
def word_list(request):
    
    qConceptUserWord = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_WORD
    ).order_by('-created')
    
    completed_count = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_WORD,
        level=10
    ).count()
    
    context = {
        'current_page' : 'word_list',
        'qConceptUserWord' : qConceptUserWord,
        'completed_count' : completed_count,
    }
    return render(request, 'study/word_list.html', context)

@login_required
def learn_new_kanji(request):
    # if too many in progress, return error message
    if request.method == 'POST':
        concept_id = request.POST.get('concept_id')
        oConcept = get_object_or_404(LearnableConcept, pk=concept_id)
        oCU, created = models.ConceptUser.objects.get_or_create(
            concept=oConcept,
            user=request.user
        )
        return redirect( request.POST.get('destination', 'study:home') )
    
    
    oConceptNextKanji = LearnableConcept.objects.filter(
        type=LearnableConcept.TYPE_KANJI,
        conceptuser__isnull=True
    ).order_by('kanji__grade', 'kanji__popularity').first()
    context = {
        'current_page' : 'learn_new_kanji',
        'oKanji' : oConceptNextKanji.kanji,
    }
    return render(request, 'study/learn_new_kanji.html', context)

@login_required
def practice_kanji_in_progress(request):
    # if too few in progress, return error message
    
    # choose a kanji
    oConceptUser = quiz.choose_a_concept(request.user)
    question, answers, correct_answer = quiz.build_a_quiz(oConceptUser)
        

     
    context = {
        'current_page' : 'practice_kanji_in_progress',
        'question' : question,
        'answers' : answers,
        'correct_answer' : correct_answer,
        'oConceptUser' : oConceptUser,
    }
    return render(request, 'study/practice_kanji_in_progress.html', context)

@login_required  
def practice_completed_kanji(request):
    # if none, return error message
    context = {
        'current_page' : 'practice_completed_kanji',
    }
    return render(request, 'study/practice_completed_kanji.html', context)















