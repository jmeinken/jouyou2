from django.contrib import admin

from . import models



class KanjiAdmin(admin.ModelAdmin):
    list_display = ('character', 
            'meaning', 'get_radical_string', 'stroke_count',
            'main_pronunciation', 'grade', 'popularity', 'jlpt_level',)
    
admin.site.register(models.Kanji, KanjiAdmin)

class RadicalAdmin(admin.ModelAdmin):
    list_display = ('character', 
            'meaning', 'stroke_count',
            'identical_kanji', 'get_kanji_string')
    
admin.site.register(models.Radical, RadicalAdmin)

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'pronunciation', 'useful', 'kanji_set_string', 'definition',  'is_proper_noun', 'popularity',  )
    filter_horizontal = ('kanji_set', )
    list_editable = ('pronunciation', 'useful', )
    
admin.site.register(models.Word, WordAdmin)
