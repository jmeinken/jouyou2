from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max

from devtools import models

from . import functions



def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))  
                return redirect('home')
            else:
                # Return a 'disabled account' error message
                context['login_error'] = 'Your account has a problem.  Please contact the administrator.'
                return render(request, 'login.html', context)
        else:
            # Return an 'invalid login' error message.
            context['login_error'] = 'Login failed.  Please reenter your username and password.'
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    print(models.testing)
    context = {
        'levels' : models.Level.objects.all(),           
    }
    return render(request, 'home.html', context)

@login_required
def level(request):
    context = {}
    if request.method == "POST":
        current_section = int(request.POST.get('current_section'))
        sectionuser = models.SectionUser.objects.get(user=request.user)
        next_section = models.Section.objects.all().filter(id__gt=current_section).aggregate(Min('id'))
        sectionuser.current_section = next_section['id__min']
        sectionuser.save()
    if not 'level' in request.GET:
        return redirect(home)
    order_number = request.GET.get('level')
    level = models.Level.objects.get(order=order_number)
    try:
        sectionuser = models.SectionUser.objects.get(user=request.user)
    except:
        first_section = models.Section.objects.all().aggregate(Min('id'))
        sectionuser = models.SectionUser(user=request.user, current_section=first_section['id__min'])
        sectionuser.save()
    context = {
        'sections' : models.Section.objects.filter(level=level),
        'current_section' : sectionuser.current_section, 
    }
    return render(request, 'level.html', context)

@login_required
def section(request):
    context = {}
    if not 'level' in request.GET and not 'section' in request.GET:
        return redirect(home)
    level_number = request.GET.get('level')
    level = models.Level.objects.get(order=level_number)
    section_number = request.GET.get('section')
    section = models.Section.objects.get(order=section_number, level=level)
    try:
        sectionuser = models.SectionUser.objects.get(user=request.user)
    except:
        first_section = models.Section.objects.all().aggregate(Min('id'))
        sectionuser = models.SectionUser(user=request.user, current_section=first_section['id__min'])
        sectionuser.save()
    context = {
        'section' : section,
        'current_section' : sectionuser.current_section, 
    }
    return render(request, 'section.html', context)

@login_required
def study(request):
    context = {}
    # temporary form handler
    if request.method == "POST":
        kanji_id = request.POST.get('kanji_id')
        kanji = models.Kanji.objects.get(pk=kanji_id)
        kanji.pronunciation = request.POST.get('pronunciation')
        kanji.meaning = request.POST.get('meaning')
        kanji.is_kanji = 'is_kanji' in request.POST
        kanji.is_image = 'is_image' in request.POST
        kanji.img_path = request.POST.get('img_path')
        kanji.comment = request.POST.get('comment')
        kanji.save()
        mnemonic = request.POST.get('mnemonic')
        example_word_ids = request.POST.getlist('example_word')
        if example_word_ids:
            example_word = models.Words.objects.get(id=example_word_ids[0])
        delete_word_ids = request.POST.getlist('delete_word')
        if delete_word_ids:
            for id in delete_word_ids:
                word = models.Words.objects.get(pk=id)
                wd = models.WordDeleted(
                    word=word.word, 
                    max_hybrid_order=word.max_hybrid_order,
                    definition=word.definition,
                    word_ranking=word.word_ranking
                )
                wd.save()
                word.delete()
        try:
            kanji_user = models.KanjiUser.objects.get(user=request.user, kanji=kanji)
            kanji_user.mnemonic = mnemonic
            print("exists")
        except:
            print("not exist")
            kanji_user = models.KanjiUser(
                user = request.user,
                kanji = kanji,
                mnemonic = mnemonic
            )
        if example_word_ids:
            print(example_word)
            kanji_user.example_word = example_word
        else:
            kanji_user.example_word = None
        kanji_user.save()
    # end temporary form handler
    if not 'level' in request.GET or not 'section' in request.GET or not 'kanji' in request.GET:
        return redirect(home)
    level_number = int(request.GET.get('level'))
    section_number = int(request.GET.get('section'))
    kanji_number = int(request.GET.get('kanji'))
    section = models.Section.objects.get(order=section_number, level__order=level_number)
    hybrid_value = section.start_kanji + kanji_number - 1
    if hybrid_value > section.end_kanji:
        return redirect(home)
    kanji = models.Kanji.objects.get(hybrid_order=hybrid_value)
    mnemonic = kanji.get_mnemonic(request.user)
    example_word = kanji.get_example_word(request.user)
    print(example_word)
    words = models.Words.objects.filter(word__contains=kanji.kanji).order_by('word_ranking')
    vocabulary = []
    for word in words:
        vocabulary.append(functions.rebuild_word_with_furigana(word))    
    try:
        pu = models.PronunciationUser.objects.get(pronunciation=kanji.pronunciation, user=request.user)
        pronunciation_mnemonic = pu.mnemonic
    except:
        pronunciation_mnemonic = ''
    context = {
        'section' : section,       
        'kanji' : kanji,
        'mnemonic' : mnemonic,
        'kanji_number' : kanji_number,
        'example_word' : example_word,
        'kanji_next' : kanji_number + 1,
        'kanji_previous' : kanji_number - 1,
        'count_in_section' : section.end_kanji - section.start_kanji + 1,
        'first' : kanji_number == 1,
        'last' : section.start_kanji + kanji_number - 1 == section.end_kanji,
        'vocab' : vocabulary,
        'pronunciation_mnemonic' : pronunciation_mnemonic
    }
    return render(request, 'study.html', context)

@login_required
def practice(request):
    context = {}
    first = False
    last = False
    if not 'level' in request.GET or not 'section' in request.GET:
        return redirect(home)
    level_number = int(request.GET.get('level'))
    section_number = int(request.GET.get('section'))
    section = models.Section.objects.get(order=section_number, level__order=level_number)
    sort_order = request.session.get('sort_section_' + str(section_number))
    if not sort_order or len(sort_order) == 0 or 'start' in request.GET:
        request.session['sort_section_' + str(section_number)] = functions.get_random_sort(section)
        sort_order = request.session.get('sort_section_' + str(section_number))
        first = True
    if len(sort_order) == 1:
        last = True
    kanji = models.Kanji.objects.get(id=sort_order.pop(0))
    request.session['sort_section_' + str(section_number)] = sort_order
    mnemonic = kanji.get_mnemonic(request.user)
    context = {
        'section' : section, 
        'kanji' : kanji,
        'mnemonic' : mnemonic,
        'first' : first,
        'last' : last,       
        'all_completed' : False,    
    }
    if request.GET.get('invert'):
        context['invert'] = True
        return render(request, 'writing_practice.html', context)
    else:
        return render(request, 'recognition_practice.html', context)

@login_required   
def practice_completed(request):
    context = {}
    sectionuser = models.SectionUser.objects.get(user=request.user)
    last_section = models.Section.objects.filter(id__lt=sectionuser.current_section).order_by('-id')[0]
    cutoff = last_section.end_kanji
    sort_order = request.session.get('sort_completed')
    set_cutoff = request.session.get('cutoff')
    if not sort_order or len(sort_order) == 0 or cutoff != set_cutoff:
        request.session['sort_completed'] = functions.get_random_sort_completed(cutoff)
        sort_order = request.session.get('sort_completed')
        request.session['cutoff'] = cutoff
    kanji = models.Kanji.objects.get(id=sort_order.pop(0))
    request.session['sort_completed'] = sort_order
    mnemonic = kanji.get_mnemonic(request.user)
    context = {
        'kanji' : kanji,
        'mnemonic' : mnemonic,    
        'all_completed' : True,   
    }
    if request.GET.get('invert'):
        context['invert'] = True
        return render(request, 'writing_practice.html', context)
    else:
        return render(request, 'recognition_practice.html', context)
    
@login_required   
def word_practice(request):
    context = {}
    first = False
    last = False
    if not 'level' in request.GET or not 'section' in request.GET:
        return redirect(home)
    level_number = int(request.GET.get('level'))
    section_number = int(request.GET.get('section'))
    section = models.Section.objects.get(order=section_number, level__order=level_number)
    sort_order = request.session.get('word_sort_section_' + str(section_number))
    if not sort_order or len(sort_order) == 0 or 'start' in request.GET:
        request.session['word_sort_section_' + str(section_number)] = functions.get_random_sort_vocab(section)
        sort_order = request.session.get('word_sort_section_' + str(section_number))
        first = True
    if len(sort_order) == 1:
        last = True
    word = models.Words.objects.get(id=sort_order.pop(0))
    word = functions.rebuild_word_with_furigana(word)
    request.session['word_sort_section_' + str(section_number)] = sort_order
    context = {
        'section' : section, 
        'word' : word,
        'first' : first,
        'last' : last,       
        'all_completed' : False,    
        'vocab_count' : functions.get_count_section_vocab(section) 
    }
    if request.GET.get('invert'):
        context['invert'] = True
        return render(request, 'writing_practice.html', context)
    else:
        return render(request, 'word_practice.html', context)

@login_required   
def word_practice_completed(request):
    context = {}
    sectionuser = models.SectionUser.objects.get(user=request.user)
    last_section = models.Section.objects.filter(id__lt=sectionuser.current_section).order_by('-id')[0]
    cutoff = last_section.end_kanji
    sort_order = request.session.get('sort_completed_vocab')
    set_cutoff = request.session.get('cutoff')
    if not sort_order or len(sort_order) == 0 or cutoff != set_cutoff:
        request.session['sort_completed_vocab'] = functions.get_random_sort_completed_vocab(cutoff)
        sort_order = request.session.get('sort_completed_vocab')
        request.session['cutoff'] = cutoff
    word = models.Words.objects.get(id=sort_order.pop(0))
    word = functions.rebuild_word_with_furigana(word)
    request.session['sort_completed_vocab'] = sort_order
    context = {
        'word' : word,   
        'all_completed' : True,  
        'vocab_count' : functions.get_count_completed_vocab(cutoff) 
    }
    return render(request, 'word_practice_completed.html', context)

@login_required
def kanji(request):
    context = {}
    if 'char' in request.GET:
        char = request.GET.get('char')
        try:
            kanji = models.Kanji.objects.get(kanji=char)
        except:
            return redirect(home)
    elif 'id' in request.GET:
        id = request.GET.get('id')
        try:
            kanji = models.Kanji.objects.get(pk=id)
        except:
            return redirect(home)
    else:
        return redirect(home)
    section = models.Section.objects.get(start_kanji__lte=kanji.hybrid_order, end_kanji__gte=kanji.hybrid_order)
    section_number = section.order
    level_number = section.level.order
    kanji_number = kanji.hybrid_order - section.start_kanji + 1
    response = redirect(study)
    response['Location'] += '?level=' + str(level_number) + "&section=" + str(section_number) + "&kanji=" + str(kanji_number)
    return response

@login_required
def word(request):
    context = {}
    if not 'word' in request.GET and not 'id' in request.GET:
        return redirect(home)
    try:
        if 'word' in request.GET:
            word = models.Words.objects.get(word=request.GET.get('word'))  
        else:
            word = models.Words.objects.get(id=request.GET.get('id'))    
    except:
        return redirect(home)
    
    context = {
         'word' : word,      
    }
    return render(request, 'word.html', context)

@login_required
def pronunciations(request):
    context = {}
    if not 'pron' in request.GET:
        return redirect(home)
    pron = request.GET['pron']
    try:
        p = models.PronunciationUser.objects.get(pronunciation=pron)
    except:
        p = models.PronunciationUser(
            user=request.user,
            pronunciation=pron                     
        )
        p.save()
    if request.method == "POST":
        p.mnemonic = request.POST.get('mnemonic')
        p.save()
    kanji = models.Kanji.objects.filter(pronunciation=pron).order_by('hybrid_order')
    context = {
        'pron' : p,
        'kanji' : kanji,
    }
    return render(request, 'pronunciations.html', context)
    
