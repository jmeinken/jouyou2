
from devtools import models


def get_random_sort(section):
    start = section.start_kanji
    end = section.end_kanji
    kanji = models.Kanji.objects.filter(is_kanji=True, hybrid_order__gte=start, hybrid_order__lte=end).order_by('?')
    result = []
    for k in kanji:
        result.append(k.id)
    return result

def get_random_sort_completed(cutoff):
    kanji = models.Kanji.objects.filter(is_kanji=True, hybrid_order__lte=cutoff).order_by('?')
    result = []
    for k in kanji:
        result.append(k.id)
    return result
        
    