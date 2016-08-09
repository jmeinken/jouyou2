
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

def get_random_sort_vocab(section):
    start = section.start_kanji
    end = section.end_kanji
    words = models.Words.objects.filter(max_hybrid_order__lte=end, max_hybrid_order__gte=start).order_by('?')
    result = []
    for w in words:
        result.append(w.id)
    return result

def get_random_sort_completed_vocab(cutoff):
    words = models.Words.objects.filter(max_hybrid_order__lte=cutoff).order_by('?')
    result = []
    for w in words:
        result.append(w.id)
    return result

def rebuild_word_with_furigana(word):
    vocab = []
    wordfurigana = models.WordFurigana.objects.filter(word=word)
    i = 1
    for char in word.word:
        fg = wordfurigana.filter(position=i)
        if fg:
            vocab.append( (char, fg[0].furigana) )
        else:
            vocab.append( (char) )
        i = i + 1
    return {
        'id' : word.id,    
        'word' : word.word,           
        'word_fg' : vocab,
        'definition' : word.definition,
        'ranking' : word.word_ranking,
        'max_hybrid_order' : word.max_hybrid_order
    }
    
def get_count_section_vocab(section):
    start = section.start_kanji
    end = section.end_kanji
    words = models.Words.objects.filter(max_hybrid_order__lte=end, max_hybrid_order__gte=start)
    i = 0
    for w in words:
        i = i + 1
    return i
    
def get_count_completed_vocab(cutoff):
    words = models.Words.objects.filter(max_hybrid_order__lte=cutoff)
    i = 0
    for w in words:
        i = i + 1
    return i
        
    