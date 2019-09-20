from django.db import models

from dictionary.models import LearnableConcept
from django.contrib.auth import get_user_model


class ConceptUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    concept = models.ForeignKey(LearnableConcept, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0)
    
class ConceptUserEncounter(models.Model):
    concept_user = models.ForeignKey(ConceptUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField()
    