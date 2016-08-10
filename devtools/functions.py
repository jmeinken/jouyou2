import sys

from . import models
import urllib
from lxml import html


def scrape_jisho(word):
    meaning = ''
    furigana = []
    url = "http://jisho.org/word/" + word.encode('utf-8')
    page = html.fromstring(urllib.urlopen(url).read())
    meaning_spans = page.xpath("//span[@class='meaning-meaning']")
    if meaning_spans:
        meaning = meaning_spans[0].text
    furigana_spans = page.xpath("//span[@class='furigana']")
    if furigana_spans:
        furigana_span = furigana_spans[0]
        for fg in furigana_span.getchildren():
            furigana.append(fg.text)
    return [
        meaning,
        furigana,
    ]    
        


def check_components_old(kanji_staging, kanji_complete, results):
    if len(kanji_staging) == 0:
        return
    kanji_id = kanji_staging[0]
    kanji = models.Kanji.objects.get(id=kanji_id)
    # results.append('starting ' + kanji.kanji)
    if kanji_id in kanji_complete:
        # results.append('removing completed kanji' + kanji.kanji)
        kanji_staging.pop(0)
        check_components(kanji_staging, kanji_complete, results)
    for kanji_component in kanji.kanji_set.all():
        component_kanji = kanji_component.component
        if component_kanji.id in kanji_complete:
            # results.append('continue because ' + component_kanji.kanji + 'already in complete for ' + kanji.kanji);
            continue
        else:
            kanji_staging.insert(0, component_kanji.id)
            # results.append('moving ' + component_kanji.kanji + 'before ' + kanji.kanji);
            check_components(kanji_staging, kanji_complete, results)
    # kanji_staging.remove(kanji.id)
    if len(kanji_staging) == 0:
        return
    # results.append('copying ' + kanji.kanji + ' to complete');
    kanji_complete.append(kanji.id)
    # kanji_staging.remove(kanji.id)
    check_components(kanji_staging, kanji_complete, results)
    
def check_components(kanji_staging, kanji_complete, results):
    sys.setrecursionlimit(10000)
    for kanji_id in kanji_staging:
        if kanji_id in kanji_complete:
            continue
        preappend_dependencies(kanji_id, kanji_complete, results, 1)
        kanji_complete.append(kanji_id)
    return
        
        
def preappend_dependencies(kanji_id, kanji_complete, results, depth):       
    kanji = models.Kanji.objects.get(id=kanji_id)
    # results.append("preappending dependencies for " + str(kanji.id) + " order " + str(kanji.most_used_order) + " depth " + str(depth))
    # print("preappending dependencies for " + str(kanji.id) + " order " + str(kanji.most_used_order) + " depth " + str(depth))
    for kanji_component in kanji.kanji_set.all():
        component_kanji = kanji_component.component
        if component_kanji.id in kanji_complete:
            continue
        else:
            preappend_dependencies(component_kanji.id, kanji_complete, results, depth+1)
            kanji_complete.append(component_kanji.id)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]





