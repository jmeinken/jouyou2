from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dictionary.models import LearnableConcept

@login_required
def home(request):
    
    oConceptNextKanji = LearnableConcept.objects.filter(
        type=LearnableConcept.TYPE_KANJI,
        conceptuser__isnull=True
    ).order_by('kanji__grade', 'kanji__popularity').first()
    
    
    # count kanji studying, kanji completed, words studying, words completed
    # get list of encountered kanji
    
    #get list of encountered words
    context = {
        'oConceptNextKanji' : oConceptNextKanji,
        'current_page' : 'home',
    }
    return render(request, 'study/home.html', context)

@login_required
def learn_new_kanji(request):
    # if too many in progress, return error message
    context = {
        'current_page' : 'learn_new_kanji',
    }
    return render(request, 'study/learn_new_kanji.html', context)

@login_required
def practice_kanji_in_progress(request):
    # if too few in progress, return error message
    context = {
        'current_page' : 'practice_kanji_in_progress',
    }
    return render(request, 'study/practice_kanji_in_progress.html', context)

@login_required  
def practice_completed_kanji(request):
    # if none, return error message
    context = {
        'current_page' : 'practice_completed_kanji',
    }
    return render(request, 'study/practice_completed_kanji.html', context)















