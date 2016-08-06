from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static




class Kanji(models.Model):
    id = models.IntegerField(primary_key=True)
    kanji = models.CharField(max_length=30)
    kd_link = models.CharField(max_length=200, null=True, blank=True)
    kd_order = models.IntegerField(null=True, blank=True) # kanji damamge order
    most_used_order = models.IntegerField(null=True, blank=True)
    hybrid_order = models.IntegerField()
    meaning = models.CharField(max_length=30, null=True, blank=True)
    is_image = models.BooleanField(default=False)
    img_path = models.CharField(max_length=100, null=True, blank=True)
    is_kanji = models.BooleanField(default=True)
    # common pronunciation (usually on-yomi)
    pronunciation = models.CharField(max_length=10, null=True, blank=True)
    on_yomi = models.CharField(max_length=50, null=True, blank=True)
    kun_yomi = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    
    def get_big_kanji(self):
        if self.is_image:
            return '<img src="' + static('img/' + self.img_path) + '" alt="test" style="padding:30px 5px"  />'
        else:
            return '<span class="text-warning" style="font-size:80px">' + self.kanji + '</span>'
        
    def get_little_kanji(self):
        if self.is_image:
            return '<!-- kanji_id=' + str(self.id) + ' --><img src="' + static('img/' + self.img_path) + '" alt="test" height="28" width="28" /><!-- end_kanji_id -->'
        else:
            return self.kanji
        
    def get_untagged_little_kanji(self):
        if self.is_image:
            return '<img src="' + static('img/' + self.img_path) + '" alt="test" height="15" width="15" />'
        else:
            return self.kanji
    
    def get_getstr(self):
        if self.is_image:
            return 'id=' + str(self.id)
        else:
            return 'char=' + self.kanji
        
    def get_mnemonic(self, user):
        try:
            kanjiuser = KanjiUser.objects.get(kanji=self,user=user)
        except:
            return ''
        return kanjiuser.mnemonic
    
    def get_example_word(self, user):
        try:
            kanjiuser = KanjiUser.objects.get(kanji=self,user=user)
            word = kanjiuser.example_word
        except:
            word = None
        return word
    
    def get_example_word_only(self, user):
        try:
            kanjiuser = KanjiUser.objects.get(kanji=self,user=user)
            word = kanjiuser.example_word.word
        except:
            word = ''
        return word
    
    
@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = ('kanji', 'hybrid_order')
             
    
class KanjiUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=500, null=True, blank=True)
    example_word = models.ForeignKey('Words', on_delete=models.CASCADE, null=True, blank=True)
    
class Morphs(models.Model):
    id = models.IntegerField(primary_key=True)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    
class KanjiComponent(models.Model):
    kanji = models.ForeignKey(Kanji, related_name = 'kanji_set')
    component = models.ForeignKey(Kanji, related_name = 'component_set')
    
class Words(models.Model):
    word = models.CharField(max_length=50)
    max_hybrid_order = models.IntegerField(null=True, blank=True)
    word_ranking = models.IntegerField(null=True, blank=True)
    definition = models.CharField(max_length=200, null=True, blank=True)
    full_pronunciation = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    
    def get_pronunciation(self):
        i = 1
        pronunciation = ''
        for char in self.word:
            try:
                fg = WordFurigana.objects.get(word=self, position=i)
                pron = fg.furigana
            except:
                pron = char
            pronunciation += pron
            i = i + 1
        return pronunciation
                
    
class WordFurigana(models.Model):
    word = models.ForeignKey(Words, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)
    furigana = models.CharField(max_length=10, null=True, blank=True)
    
testing = "hello"    

class Level(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    order = models.IntegerField()

class Section(models.Model):
    order = models.IntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    start_kanji = models.IntegerField()
    end_kanji = models.IntegerField()
    
class SectionUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_section = models.IntegerField(default=0)  # the section ID

    