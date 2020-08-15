from django.db import models

from dictionary.models import LearnableConcept
# from user_manager.models import User



class UserBadge(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user_manager.User', on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=120)
    user_alerted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (("user", "badge_name"),)


def get_concept_user_for_concept(oConcept, oUser):
    oConceptUser = ConceptUser.objects.filter(concept=oConcept, user=oUser).first()
    return oConceptUser


class ConceptUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user_manager.User', on_delete=models.CASCADE)
    concept = models.ForeignKey(LearnableConcept, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    
    def get_level_pretty(self):
#         if self.level == 10:
#             return self.get_level_pretty_old()
        response = []
        filled_circle = '<i class="fa fa-circle level-indicator" aria-hidden="true"></i>'
        check_circle = '<i class="fa fa-check-circle level-indicator" aria-hidden="true"></i>'
        large_circle = '<i class="fa fa-circle fa-lg level-indicator" aria-hidden="true"></i>'
        empty_circle = '<i class="fa fa-circle-thin text-muted level-indicator" aria-hidden="true"></i>'
        large_empty_circle = '<i class="fa fa-circle-thin fa-lg text-muted level-indicator" aria-hidden="true"></i>'
        response.append('<span class="text-danger">')
        response.append(filled_circle if 1 <= self.level else empty_circle)
        response.append(filled_circle if 2 <= self.level else empty_circle)
        response.append(filled_circle if 3 <= self.level else empty_circle)
        response.append(filled_circle if 4 <= self.level else empty_circle)
        response.append(filled_circle if 5 <= self.level else empty_circle)
        response.append('</span>')
        response.append('<span class="text-warning">')
        response.append(filled_circle if 6 <= self.level else empty_circle)
        response.append(filled_circle if 7 <= self.level else empty_circle)
        response.append(filled_circle if 8 <= self.level else empty_circle)
        
        response.append('</span>')
        response.append('<span class="text-success">')
        response.append(filled_circle if 9 <= self.level else empty_circle)
        response.append(large_circle if 10 <= self.level else large_empty_circle)
        response.append('</span>')
        return ' '.join(response)
        
    
    def get_level_pretty_old(self):
        if self.level <=5:
            color='text-danger'
        elif self.level < 10:
            color='text-warning'
        else:
            color='text-success'
        response = []
        for i in range(10):
            if self.level == 10:
                response.append('<i class="fa fa-circle {}" aria-hidden="true"></i>'.format(color))
            elif i < self.level:
                response.append('<i class="fa fa-circle {}" aria-hidden="true"></i>'.format(color))
            else:
                response.append('<i class="fa fa-circle-thin {}" aria-hidden="true"></i>'.format(color))
        return ' '.join(response)
    
    def attempt_to_unlock_related_words(self):
        if not self.level == 10:
            return
        oUser = self.user
        # concept must be a kanji or this doesn't make sense
        if not self.concept.type == 'kanji':
            return
        # get all words that contain this kanji and have not already been unlocked
        qWord = self.concept.kanji.word_set.filter(useful=True)
        qWord = qWord.exclude(concept__conceptuser__user=oUser)
        # for each word, check if all kanji are completed
        words = []
        for oWord in qWord:
            print(oWord)
            if get_concept_user_for_concept(oWord.concept, oUser):
                continue
            word_complete = True
            for oKanji in oWord.kanji_set.all():
                oCU = get_concept_user_for_concept(oKanji.concept, oUser)
                if not oCU or oCU.level < 10:
                    word_complete = False
            if word_complete:
                oConceptUser = ConceptUser(concept=oWord.concept, user=oUser)
                oConceptUser.save()
                words.append(oConceptUser.concept.word)
        return words
                
            
        
    
class ConceptUserEncounter(models.Model):
    concept_user = models.ForeignKey(ConceptUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField()
    