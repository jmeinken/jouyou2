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
    list_display = ('word', 'kanji_set_string', 'definition', 'pronunciation', 'is_proper_noun', 'popularity')
    
admin.site.register(models.Word, WordAdmin)
