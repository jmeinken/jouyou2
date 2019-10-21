



from django.dispatch import receiver
from django.db import models

from .models import ConceptUser, UserBadge
from .badges import badge_list, check_if_badge_earned 



def get_concept_user_for_concept(oConcept, oUser):
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=oUser).first()
    return oConceptUser

@receiver(models.signals.post_save, sender=ConceptUser)
def unlock_words_associated_with_kanji(sender, instance, created, **kwargs):
    # instance.attempt_to_unlock_related_words()
    pass


@receiver(models.signals.post_save, sender=ConceptUser)
def unlock_badges(sender, instance, created, **kwargs):
    if instance.level != 10:
        return
    badges_earned = UserBadge.badges_earned()
    for badge_name, entry in badge_list.items():
        if not badge_name in badges_earned and check_if_badge_earned(badge_name, instance.user):
            oBadge = UserBadge(user=instance.user, badge_name=badge_name)
            oBadge.save()
                
            
    
    