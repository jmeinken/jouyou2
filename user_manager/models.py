from __future__ import unicode_literals


from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

from study.models import ConceptUser
from dictionary.models import LearnableConcept


class User(AbstractUser):
    
    def score(self):
        qConcept = self.conceptuser_set.all()
        score = qConcept.aggregate(score=Sum('level'))
        return score['score']

    def allowed_to_learn_new_kanji(self):
        qConcept = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_KANJI,
            level__lt=10
        )
        return True if qConcept.count() <= 50 else False
      
    def allowed_to_practice_unfinished_kanji(self):
        qConcept = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_KANJI,
            level__lt=10
        )
        return True if qConcept.count() >= 10 else False
    
    def allowed_to_practice_unfinished_words(self):
        qConcept = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_WORD,
            level__lt=10
        )
        return True if qConcept.count() >= 10 else False
       
    def allowed_to_practice_completed_kanji(self):
        qConcept = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_KANJI,
            level=10
        )
        return True if qConcept.count() >= 20 else False
    
    def count_completed_kanji(self):
        qCU = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_KANJI,
            level=10
        )
        return qCU.count()
        
    def count_completed_words(self):
        qCU = ConceptUser.objects.filter(
            user=self,
            concept__type=LearnableConcept.TYPE_WORD,
            level=10
        )
        return qCU.count()
    
    
    
    
    
    
    
    
    
    
    