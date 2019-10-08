



from django.dispatch import receiver
from django.db import models

from .models import ConceptUser



def get_concept_user_for_concept(oConcept, oUser):
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=oUser).first()
    return oConceptUser

@receiver(models.signals.post_save, sender=ConceptUser)
def unlock_words_associated_with_kanji(sender, instance, created, **kwargs):
    # instance.attempt_to_unlock_related_words()
    pass