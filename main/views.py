from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
def levels(request):
    context = {}
    if not 'level' in request.GET:
        return redirect(home)
    order_number = request.GET.get('level')
    level = models.Level.objects.get(order=order_number)
    context = {
        'sections' : models.Section.objects.filter(level=level),       
    }
    return render(request, 'level.html', context)

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
        if mnemonic:
            kanji_user = models.KanjiUser(
                user = request.user,
                kanji = kanji,
                mnemonic = mnemonic
            )
            kanji_user.save()
        kanji_number = int(request.POST.get('kanji_number'))
        section = models.Section.objects.get(start_kanji__lte=kanji.hybrid_order, end_kanji__gte=kanji.hybrid_order)
        context = {
            'section' : section,       
            'kanji' : kanji,
            'mnemonic' : mnemonic,
            'kanji_number' : kanji_number,
            'kanji_next' : kanji_number + 1,
            'kanji_previous' : kanji_number - 1,
            'first' : kanji_number == 1,
            'last' : section.start_kanji + kanji_number - 1 == section.end_kanji
        }
        return render(request, 'study.html', context)
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
    try:
        mnemonic = models.KanjiUser.objects.get(kanji=kanji,user=request.user).mnemonic
    except:
        mnemonic = None
    context = {
        'section' : section,       
        'kanji' : kanji,
        'mnemonic' : mnemonic,
        'kanji_number' : kanji_number,
        'kanji_next' : kanji_number + 1,
        'kanji_previous' : kanji_number - 1,
        'first' : kanji_number == 1,
        'last' : section.start_kanji + kanji_number - 1 == section.end_kanji
    }
    return render(request, 'study.html', context)

@login_required
def kanji(request):
    context = {}
    if not 'char' in request.GET:
        return redirect(home)
    char = request.GET.get('char')
    try:
        kanji = models.Kanji.objects.get(kanji=char)
    except:
        return redirect(home)
    context = {
         'kanji' : kanji,      
    }
    return render(request, 'kanji.html', context)

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

