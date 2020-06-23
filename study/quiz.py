
import random

from django.template.loader import render_to_string

from . import models
from dictionary.models import LearnableConcept, Kanji, Word



def choose_a_concept(oUser, 
        include_unfinished=True, include_completed=True, 
        include_kanji=True, include_words=True
    ):
    oCU = models.ConceptUser.objects.filter(user=oUser)
    if include_kanji and not include_words:
        oCU = oCU.filter(concept__type=LearnableConcept.TYPE_KANJI)
    elif include_words and not include_kanji:
        oCU = oCU.filter(concept__type=LearnableConcept.TYPE_WORD)
    if include_unfinished and not include_completed:
        oCU = oCU.filter(level__lt=10)
    elif include_completed and not include_unfinished:
        oCU = oCU.filter(level=10)
    oCU = oCU.order_by('modified')[:5]
    max_length = oCU.count() - 1
    return oCU[random.randint(0,max_length)]

def choose_a_concept_old(oUser, 
        include_unfinished=True, include_completed=True, 
        include_kanji=True, include_words=True):
    oCU = models.ConceptUser.objects.filter(
        user=oUser, 
        concept__type=LearnableConcept.TYPE_KANJI,
        level__lt=10
    ).order_by('modified')[:5]
    max_length = oCU.count() - 1
    return oCU[random.randint(0,max_length)]

def choose_a_word(oUser):
    oCU = models.ConceptUser.objects.filter(
        user=oUser, 
        concept__type=LearnableConcept.TYPE_WORD,
        level__lt=10
    ).order_by('modified')[:5]
    max_length = oCU.count() - 1
    return oCU[random.randint(0,max_length)]

def build_a_quiz_for_word(oCU):
    question = oCU.concept.word.word
    # create answers list
    quiz_types = ['pronunciation', 'definition']
    quiz_type = random.choice(quiz_types)
    answers = []
    if quiz_type == 'definition':
        correct_answer = oCU.concept.word.get_simplified_definition()
    else:
        correct_answer = getattr(oCU.concept.word, quiz_type)
    exclude = {quiz_type: correct_answer}
    qWord = Word.objects.exclude(**exclude).order_by('?')[:3]
    answers.append( [correct_answer, 1] )
    for oWord in qWord:
        if quiz_type == 'definition':
            answers.append( [oWord.get_simplified_definition(), 0] )
        else:
            answers.append( [getattr(oWord, quiz_type), 0] )
    random.shuffle(answers)
    correct_answer_string = render_to_string('study/snippets/word_quick_details.html', {'oWord' : oCU.concept.word})
    return (question, answers, correct_answer_string)

def build_a_quiz(oCU):
    if oCU.concept.type == oCU.concept.TYPE_WORD:
        return build_a_quiz_for_word(oCU)
    question = oCU.concept.kanji.character
    # create answers list
    quiz_types = ['main_pronunciation', 'meaning']
    quiz_type = random.choice(quiz_types)
    answers = []
    if quiz_type == 'meaning':
        correct_answer = oCU.concept.kanji.get_simplified_meaning()
    else:
        correct_answer = getattr(oCU.concept.kanji, quiz_type)
    exclude = {quiz_type: correct_answer}
    qKanji = Kanji.objects.exclude(**exclude).order_by('?')[:3]
    answers.append( [correct_answer, 1] )
    for oKanji in qKanji:
        if quiz_type == 'meaning':
            answers.append( [oKanji.get_simplified_meaning(), 0] )
        else:
            answers.append( [getattr(oKanji, quiz_type), 0] )
    random.shuffle(answers)
    correct_answer_string = render_to_string('study/snippets/kanji_quick_details.html', {'oKanji' : oCU.concept.kanji})
    return (question, answers, correct_answer_string)
    