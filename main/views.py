from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Min

from devtools import models



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
        if mnemonic or mnemonic == '':
            try:
                kanji_user = models.KanjiUser.objects.get(user=request.user, kanji=kanji)
                kanji_user.mnemonic = mnemonic
                print "exists"
            except:
                print "not exist"
                kanji_user = models.KanjiUser(
                    user = request.user,
                    kanji = kanji,
                    mnemonic = mnemonic
                )
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
    words = models.Words.objects.filter(word__contains=kanji.kanji).order_by('word_ranking')
    vocabulary = []
    for word in words:
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
        vocabulary.append({
            'word' : vocab,
            'definition' : word.definition,
            'ranking' : word.word_ranking,
        })    
    context = {
        'section' : section,       
        'kanji' : kanji,
        'mnemonic' : mnemonic,
        'kanji_number' : kanji_number,
        'kanji_next' : kanji_number + 1,
        'kanji_previous' : kanji_number - 1,
        'count_in_section' : section.end_kanji - section.start_kanji + 1,
        'first' : kanji_number == 1,
        'last' : section.start_kanji + kanji_number - 1 == section.end_kanji,
        'vocab' : vocabulary
    }
    return render(request, 'study.html', context)

def practice(request):
    context = {}
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
    context = {
        'section' : section, 
        'kanji' : kanji,
        'mnemonic' : mnemonic,
        'kanji_number' : kanji_number,
        'kanji_next' : kanji_number + 1,
        'kanji_previous' : kanji_number - 1,
        'count_in_section' : section.end_kanji - section.start_kanji + 1,
        'first' : kanji_number == 1,
        'last' : section.start_kanji + kanji_number - 1 == section.end_kanji,       
    }
    if request.GET.get('invert'):
        return render(request, 'writing_practice.html', context)
    else:
        return render(request, 'recognition_practice.html', context)

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

