from django.shortcuts import render, redirect

from devtools.models import Kanji

# Create your views here.


def home(request):
    context = {}
    return render(request, 'home.html', context)

def kanji(request):
    context = {}
    if not 'char' in request.GET:
        return redirect(home)
    char = request.GET.get('char')
    try:
        kanji = Kanji.objects.get(kanji=char)
    except:
        return redirect(home)
    context = {
         'kanji' : kanji,      
    }
    return render(request, 'kanji.html', context)

