import re

from django import template

from devtools import models




register = template.Library()


def tag_kanji(value, user):
    """Create popovers for all kanji in provided string"""
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
    title = kanji.get_untagged_little_kanji().replace('"',"'") + pron + ' - ' + kanji.meaning
    content = mnemonic + "<br><a href='/kanji?" + kanji.get_getstr() + "'>[more]</a>"
    output = (output + '<a  class="clickable-kanji" data-container="body" data-toggle="popover" data-placement="top" data-html="true"' +
            ' data-content="' + content + '"' +
            ' title="' + title + '">')
    return output








