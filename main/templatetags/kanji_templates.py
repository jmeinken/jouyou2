import re

from django import template
from django.conf import settings

from devtools import models




register = template.Library()


def tag_kanji(value, user):
    """Create popovers for all kanji in provided string"""
    # {{mystr|tag_kanji:user|safe}}
    output = ""
    for char in value:
        try:
            kanji = models.Kanji.objects.get(kanji=char)
        except:
            output = output + char
            continue
        output = (output + get_popover(kanji, user) + char +'</a>')
    match = re.search(r'<!-- kanji_id=(\d*) -->', output)
    while match:
       id = int(match.group(1))
       kanji = models.Kanji.objects.get(pk=id)
       output = re.sub(match.group(0), get_popover(kanji, user), output)
       match = re.search(r'<!-- kanji_id=(\d*) -->', output)
    output = re.sub(r'<!-- end_kanji_id -->', r'</a>', output)
    return output

register.filter('tag_kanji', tag_kanji)

def tag_pronunciation(value, user):
    """Create popovers for a pronunciation"""
    try:
        p = models.PronunciationUser.objects.get(pronunciation=value)
    except:
        return value + ' <a href="/pronunciations?pron=' + value + '">[mnemonic]</a>'
    output = value + ' <a href="/pronunciations?pron=' + value + '">[mnemonic]</a>'
    return output

register.filter('tag_pronunciation', tag_pronunciation)

   

def get_popover(kanji, user):
    """Returns opening <a> tag only"""
    output = ""
    try:
        kanjiuser = models.KanjiUser.objects.get(kanji=kanji, user=user)
        mnemonic = kanjiuser.mnemonic.replace('"',"'")
    except:
        mnemonic = ''
    if kanji.pronunciation:
        pron = '&nbsp;&nbsp;&nbsp;(' + kanji.pronunciation + ')'
    else:
        pron = ''
    example_word = kanji.get_example_word(user)
    title = kanji.get_untagged_little_kanji().replace('"',"'") + pron + ' - ' + kanji.meaning
    content = ''
    subfolder="/jouyou/"
    if example_word:
        content = 'example word: ' + example_word.word + ' (' + example_word.get_pronunciation() + ')<br>'
    content = content + mnemonic + "<br><a href='" + subfolder + "kanji?" + kanji.get_getstr() + "'>[more]</a>"
    output = (output + '<a  class="clickable-kanji" data-container="body" data-toggle="popover" data-placement="top" data-html="true"' +
            ' data-content="' + content + '"' +
            ' title="' + title + '">')
    return output








