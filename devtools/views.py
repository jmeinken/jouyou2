import urllib
from lxml import html
import time

from django.shortcuts import render, redirect
from django.db import connection




from . import models
from .functions import check_components, scrape_jisho

# Create your views here.


def dashboard(request):
    context = {
        'action' : 'scrape kanjidamage site',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
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
    context = {
        'action' : 'import data from kanji_table.txt',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
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
            meaning = spl[5],
            pronunciation = spl[6],
        )
        m.save()
        results.append(spl[1])
    context = {
        'results' : results,       
    }
    return render(request, 'devtools/start_action.html', context)

def  import_kanji_component_data(request):
    context = {
        'action' : 'import data from kanji_component_table.txt',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
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
    return render(request, 'devtools/start_action.html', context)

def hybrid_sort(request):
    context = {
        'action' : 'sort kanji using hybrid sort',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
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
    return render(request, 'devtools/start_action.html', context)

def import_words(request):
    context = {
        'action' : 'add words from word_table.com to database',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
    results = []
    file = open('/home/ubuntu/django/jouyou-env/jouyou/devtools/data/word_table.txt', 'r')
    #x = 1
    for line in file:
        #x = x+1
        #if x == 200:
        #    break
        fields = line.strip().split('\t')
        ranking = fields[0]
        word = fields[1].decode('utf-8')
        # continue if word already exists in db
        if models.Words.objects.filter(word=word):
            continue
        hybrid_orders = []
        for char in word:
            try:
                kanji = models.Kanji.objects.get(kanji=char)
            except:
                kanji = None
            if not kanji is None:
                hybrid_orders.append(kanji.hybrid_order)
        if not hybrid_orders:
            continue
        max_hybrid = max(hybrid_orders)
        meaning, furigana = scrape_jisho(word)
        if not meaning:
            continue
        w = models.Words(
            word = word, 
            max_hybrid_order = max_hybrid,
            word_ranking = ranking,
            definition = meaning,
        )
        w.save()
        i = 1
        for fg in furigana:
            if not fg is None:
                f = models.WordFurigana(
                    word = w, 
                    position = i,
                    furigana = fg
                )
                f.save()
            i = i + 1
        results.append({
            'word' : word,
            'ranking' : ranking,
            'max_hybrid' : max_hybrid,
            'def' : meaning,
            'furigana' : furigana,
        })
    context['results'] = results
    return render(request, 'devtools/start_action.html', context)

def populate_level(request):
    context = {
        'action' : 'erase and repopulate level table',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
    models.Level.objects.all().delete()
    level = models.Level(
        name = 'Level 1',
        label = 'First 100',
        order = 1
    )
    level.save()
    level = models.Level(
        name = 'Level 2',
        label = '101 - 300',
        order = 2
    )
    level.save()
    level = models.Level(
        name = 'Level 3',
        label = '301-500',
        order = 3
    )
    level.save()
    results = models.Level.objects.all()
    context['results'] = results
    return render(request, 'devtools/start_action.html', context)

    
def populate_section(request):
    context = {
        'action' : 'erase and repopulate section table',
    }
    if request.method != "POST":
        return render(request, 'devtools/start_action.html', context)
    models.Section.objects.all().delete()
    level = models.Level.objects.get(order=1)
    section_arr = [0, 15, 30, 45, 60, 75, 90, 100]
    add_section(level, section_arr)
    level = models.Level.objects.get(order=2)
    section_arr = [100, 115, 130, 145, 160, 175, 190, 200, 215, 230, 245, 260, 275, 290, 300]
    add_section(level, section_arr)
    level = models.Level.objects.get(order=3)
    section_arr = [300, 315, 330, 345, 360, 375, 390, 400, 415, 430, 445, 460, 475, 490, 500]
    add_section(level, section_arr)
    results = models.Section.objects.all()
    context['results'] = results
    
    return render(request, 'devtools/start_action.html', context)

def add_section(level, section_arr):
    i = 0
    for section in section_arr:
        if i == 0:
            i = i + 1
            continue
        section = models.Section(
            order = i,
            level = level,
            start_kanji = section_arr[i-1]+1,
            end_kanji = section_arr[i]
        )
        section.save()
        i = i + 1
    return