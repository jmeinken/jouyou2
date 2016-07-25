from __future__ import unicode_literals

from django.db import models
from django.contrib import admin




class Kanji(models.Model):
    id = models.IntegerField(primary_key=True)
    kanji = models.CharField(max_length=30)
    kd_link = models.CharField(max_length=200, null=True, blank=True)
    kd_order = models.IntegerField(null=True, blank=True) # kanji damamge order
    most_used_order = models.IntegerField(null=True, blank=True)
    hybrid_order = models.IntegerField()
    meaning = models.CharField(max_length=30, null=True, blank=True)
    is_image = models.BooleanField(default=False)
    is_kanji = models.BooleanField(default=True)
    # common pronunciation (usually on-yomi)
    pronunciation = models.CharField(max_length=10, null=True, blank=True)
    on_yomi = models.CharField(max_length=50, null=True, blank=True)
    kun_yomi = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    
class Morphs(models.Model):
    id = models.IntegerField(primary_key=True)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    
class KanjiComponent(models.Model):
    kanji = models.ForeignKey(Kanji, related_name = 'kanji_set')
    component = models.ForeignKey(Kanji, related_name = 'component_set')
    
class Words(models.Model):
    word = models.CharField(max_length=50)
    max_hybrid_order = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    