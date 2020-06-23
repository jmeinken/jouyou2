from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dictionary.models import LearnableConcept
from . import models
from . import quiz
from .badges import badge_list






@login_required
def practice(request):
    # if fewer than 15 kanji in active list, do a new kanji
    active_kanji_count = models.ConceptUser.objects.filter(
        user=request.user, concept__type=LearnableConcept.TYPE_KANJI, level__lt=10
    ).count()
    if active_kanji_count < 15:
        oConceptNextKanji = LearnableConcept.objects.exclude(
                conceptuser__user=request.user,
            ).filter(
            type=LearnableConcept.TYPE_KANJI
        ).order_by('kanji__grade', 'kanji__popularity').first()
        oConceptUser, created = models.ConceptUser.objects.get_or_create(
            concept=oConceptNextKanji,
            user=request.user
        )
    else:
        # else select an existing unfinished concept (kanji or word)
        oConceptUser = quiz.choose_a_concept(request.user, include_completed=False)
    # prepare the quiz for the selected concept
    question, answers, correct_answer = quiz.build_a_quiz(oConceptUser)
    context = {
        'current_page' : 'practice',
        'question' : question,
        'answers' : answers,
        'correct_answer' : correct_answer,
        'oConceptUser' : oConceptUser,
    }
    return render(request, 'study/practice.html', context)

@login_required
def review(request):
    # if fewer than 15 kanji in active list, do a new kanji
    finished_concept_count = models.ConceptUser.objects.filter(
        level=10, user=request.user, 
    ).count()
    print(finished_concept_count)
    if finished_concept_count < 15:
        return render(request, 'study/review_not_ready.html', {})
    else:
        # else select an existing unfinished concept (kanji or word)
        oConceptUser = quiz.choose_a_concept(request.user, include_completed=False)
    # prepare the quiz for the selected concept
    question, answers, correct_answer = quiz.build_a_quiz(oConceptUser)
    context = {
        'current_page' : 'review',
        'question' : question,
        'answers' : answers,
        'correct_answer' : correct_answer,
        'oConceptUser' : oConceptUser,
    }
    return render(request, 'study/review.html', context)





@login_required
def home(request):
    
    qConceptUserKanji = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_KANJI
    ).order_by('created')
    
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
def badges(request):
    earned_badges = ['money man', 'high roller', 'kanji baby']
    earned_badges = request.user.badges_earned()
    request.user.mark_new_badges_viewed()
    context = {
        'current_page' : 'badges',
        'badge_list' : badge_list,
        'earned_badges' : earned_badges,
    }
    return render(request, 'study/badges.html', context)

@login_required
def word_list(request):
    
    qConceptUserWord = models.ConceptUser.objects.filter(
        user=request.user,
        concept__type=LearnableConcept.TYPE_WORD
    ).order_by('created')
    
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
def practice_words_in_progress(request):
    # if too few in progress, return error message
    
    # choose a kanji
    oConceptUser = quiz.choose_a_word(request.user)
    question, answers, correct_answer = quiz.build_a_quiz_for_word(oConceptUser)
        

     
    context = {
        'current_page' : 'practice_words_in_progress',
        'question' : question,
        'answers' : answers,
        'correct_answer' : correct_answer,
        'oConceptUser' : oConceptUser,
    }
    return render(request, 'study/practice_words_in_progress.html', context)



@login_required  
def practice_completed_kanji(request):
    # if none, return error message
    context = {
        'current_page' : 'practice_completed_kanji',
    }
    return render(request, 'study/practice_completed_kanji.html', context)















