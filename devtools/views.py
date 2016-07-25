import urllib
from lxml import html
import time

from django.shortcuts import render, redirect
from django.db import connection

import sys


from . import models

# Create your views here.


def dashboard(request):
    context = {}
    context['results'] = []
    url = "http://www.kanjidamage.com/kanji"
    page = html.fromstring(urllib.urlopen(url).read())
    x = 1
    # loop thru all links on page
    for link in page.xpath("//a"):
        href = link.get("href")
        if href and href.find('/kanji/') != -1:
            url2 = 'http://www.kanjidamage.com' + link.get("href")
            page2 = html.fromstring(urllib.urlopen(url2).read())
            radical_urls = []
            h1 = page2.xpath("//h1")[0]
            next = h1.getnext()
            while not next is None:
                radical_urls.append(next.get("href"))
                next = next.getnext()
            context['results'].append({
                 "kanji" : link.text,
                 "url" : link.get("href"),
                 'radical_urls' : radical_urls,
                 'id' : x,
            })
            time.sleep(0.05)
            x = x + 1
            #if x == 30:
            #    break
    for result in context['results']:
        radicals = []
        for radical in result['radical_urls']:
            for result2 in context['results']: 
                if result2["url"] == radical:
                    rad = result2
                    radicals.append( {
                        'kanji' : rad['kanji'],
                        'id' : rad['id'],
                        'url' : rad['url'],
                    } )
        result['radicals'] = radicals
    return render(request, 'devtools/dashboard.html', context)

def  import_kanji_data(request):
    context = {}
    file = open('/home/ubuntu/django/jouyou-env/jouyou/devtools/data/kanji_table.txt', 'r')
    results = []
    is_first_line = True
    for line in file:
        if is_first_line:
            is_first_line = False
            continue
        spl = line.rstrip('\n').split('\t')
        spl[0] = int(spl[0])
        spl[4] = int(spl[4])
        try:
            spl[3] = int(spl[3])
        except:
            spl[3] = None
        m = models.Kanji(
            id = spl[0],
            kanji = spl[1],
            kd_order = spl[0],
            kd_link = spl[2],
            most_used_order = spl[3],
            hybrid_order = spl[4],
        )
        m.save()
        results.append(spl[1])
    context = {
        'results' : results,       
    }
    return render(request, 'devtools/import_data.html', context)

def  import_kanji_component_data(request):
    context = {}
    file = open('/home/ubuntu/django/jouyou-env/jouyou/devtools/data/kanji_component_table.txt', 'r')
    results = []
    is_first_line = True
    for line in file:
        if is_first_line:
            is_first_line = False
            continue
        spl = line.rstrip('\n').split('\t')
        try:
            spl[0] = int(spl[0])
        except:
            spl[0] = None
        try:
            spl[2] = int(spl[2])
        except:
            spl[2] = None
        m = models.KanjiComponent(
            kanji = models.Kanji.objects.get(pk=spl[0]),
            component = models.Kanji.objects.get(pk=spl[2]),
        )
        m.save()
        results.append(spl[0])
    context = {
        'results' : results,       
    }
    return render(request, 'devtools/import_data.html', context)

def hybrid_sort(request):
    context = {}
    results = []
    kanji_queryset = models.Kanji.objects.all().exclude(most_used_order__isnull=True).order_by('most_used_order')
    # results.append('start');
    kanji_staging = []
    kanji_complete = []
    for kanji in kanji_queryset:
        kanji_staging.append(kanji.id)
        # results.append(kanji.kanji);
    # kanji_all = models.Kanji.objects.all().order_by('most_used_order')
    check_components(kanji_staging, kanji_complete, results)
    results.append('finish');
    for kanji_id in kanji_complete:
        kanji = models.Kanji.objects.get(id=kanji_id)
        # results.append(kanji.id);
        results.append(str(kanji.id) + '\t' + kanji.kanji);
    context = {
        'results' : results,       
    }
    return render(request, 'devtools/import_data.html', context)

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







