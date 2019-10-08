
import random

from . import models
from dictionary.models import LearnableConcept, Kanji


def choose_a_concept(oUser, 
        include_unfinished=True, include_completed=True, 
        include_kanji=True, include_words=True):
    oCU = models.ConceptUser.objects.filter(
        user=oUser, 
        concept__type=LearnableConcept.TYPE_KANJI,
        level__lt=10
    ).order_by('modified').first()
    return oCU

def build_a_quiz(oCU):
    question = oCU.concept.kanji.character
    # create answers list
    quiz_types = ['main_pronunciation', 'meaning']
    quiz_type = random.choice(quiz_types)
    answers = []
    correct_answer = getattr(oCU.concept.kanji, quiz_type)
    exclude = {quiz_type: correct_answer}
    qKanji = Kanji.objects.exclude(**exclude).order_by('?')[:3]
    answers.append( [correct_answer, 1] )
    for oKanji in qKanji:
        answers.append( [getattr(oKanji, quiz_type), 0] )
    random.shuffle(answers)
    return (question, answers)
    