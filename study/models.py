from django.db import models

from dictionary.models import LearnableConcept
from django.contrib.auth import get_user_model


class ConceptUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    concept = models.ForeignKey(LearnableConcept, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0)
    
    def get_level_pretty(self):
        if self.level <=5:
            color='text-danger'
        elif self.level < 10:
            color='text-warning'
        else:
            color='text-light'
        response = []
        for i in range(10):
            if self.level == 10:
                response.append('<i class="fa fa-check-circle {}" aria-hidden="true"></i>'.format(color))
            elif i < self.level:
                response.append('<i class="fa fa-circle {}" aria-hidden="true"></i>'.format(color))
            else:
                response.append('<i class="fa fa-circle-thin {}" aria-hidden="true"></i>'.format(color))
        return ' '.join(response)
                
            
        
    
class ConceptUserEncounter(models.Model):
    concept_user = models.ForeignKey(ConceptUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField()
    