

from study import models
from dictionary.models import LearnableConcept


# def user_can_learn_new_kanji(oUser):
#     qConcept = models.ConceptUser.objects.filter(
#         user=oUser,
#         concept__type=LearnableConcept.TYPE_KANJI,
#         level__lt=10
#     )
#     return True if qConcept.count() <= 50 else False
# 
# def user_can_practice_unfinished_kanji(oUser):
#     qConcept = models.ConceptUser.objects.filter(
#         user=oUser,
#         concept__type=LearnableConcept.TYPE_KANJI,
#         level__lt=10
#     )
#     return True if qConcept.count() >= 20 else False
# 
# def user_can_practice_completed_kanji(oUser):
#     qConcept = models.ConceptUser.objects.filter(
#         user=oUser,
#         concept__type=LearnableConcept.TYPE_KANJI,
#         level=10
#     )
#     return True if qConcept.count() >= 20 else False
    

def nav_options_processor(request):
    return {
#         'user_can_learn_new_kanji' : user_can_learn_new_kanji(request.user),
#         'user_can_practice_unfinished_kanji' : user_can_practice_unfinished_kanji(request.user),
#         'user_can_practice_completed_kanji' : user_can_practice_completed_kanji,
    }