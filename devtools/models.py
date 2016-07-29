from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User




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
    
class KanjiUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=200, null=True, blank=True)
    
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
    
class WordFurigana(models.Model):
    word = models.ForeignKey(Words, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)
    furigana = models.CharField(max_length=10, null=True, blank=True)
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)

    