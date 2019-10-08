



from django.dispatch import receiver
from django.db import models

from .models import ConceptUser



def get_concept_user_for_concept(oConcept, oUser):
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=oUser).first()
    return oConceptUser

@receiver(models.signals.post_save, sender=ConceptUser)
def unlock_words_associated_with_kanji(sender, instance, created, **kwargs):
    if not instance.level == 10:
        return
    oUser = instance.user
    # concept must be a kanji or this doesn't make sense
    if not instance.concept.type == 'kanji':
        return
    # get all words that contain this kanji and have not already been unlocked
    qWord = instance.concept.kanji.word_set.all()
    qWord = qWord.filter(concept__conceptuser__user=oUser)
    print('qWord', qWord)
    # for each word, check if all kanji are completed
    for oWord in qWord:
        print(oWord)
        if get_concept_user_for_concept(oWord.concept, oUser):
            continue
        word_complete = True
        for oKanji in oWord.kanji_set.all():
            if not get_concept_user_for_concept(oKanji.concept, oUser):
                word_complete = False
        if word_complete:
            oConceptUser = ConceptUser(concept=oWord.concept, user=oUser)
            oConceptUser.save()