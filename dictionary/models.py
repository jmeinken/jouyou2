from django.db import models


class LearnableConcept(models.Model):
    TYPE_KANJI = 'kanji'
    TYPE_WORD = 'word'
    TYPE_CHOICES = (
        (TYPE_KANJI, TYPE_KANJI),
        (TYPE_WORD, TYPE_WORD),
    )
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)

class Radical(models.Model):
    character               = models.CharField(max_length=1, unique=True)
    meaning                 = models.CharField(max_length=255, null=True, blank=True)
    stroke_count            = models.IntegerField(null=True, blank=True)
    identical_kanji         = models.ForeignKey('Kanji', 
                                    on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_kanji_string(self):
        qKanji = self.kanji_set.all()
        kanji = []
        for oKanji in qKanji:
            kanji.append(oKanji.character)
        return ', '.join(kanji)

class Kanji(models.Model):
    # learnable concept is optional right now because I don't plan on teaching radicals
    concept             = models.OneToOneField(LearnableConcept, on_delete=models.CASCADE)
    character               = models.CharField(max_length=1, unique=True)
    meaning             = models.CharField(max_length=255, null=True, blank=True)
    main_pronunciation  = models.CharField(max_length=10, null=True, blank=True)
    stroke_count        = models.IntegerField(null=True, blank=True)
    grade               = models.IntegerField(null=True, blank=True)
    popularity          = models.IntegerField(null=True, blank=True)
    jlpt_level          = models.IntegerField(null=True, blank=True)
    hybrid_order        = models.IntegerField(null=True, blank=True)
    comment             = models.CharField(max_length=1000, null=True, blank=True)
    radicals            = models.ManyToManyField("Radical", blank=True)
    
    class Meta:
        ordering = ['popularity']
    
    def __str__(self):
        return self.character

    def get_radical_string(self):
        qRadical = self.radicals.all()
        radicals = []
        for oRadical in qRadical:
            if oRadical.meaning:
                radicals.append( '{} ({})'.format(oRadical.character, oRadical.meaning) )
            else:
                radicals.append(oRadical.character)
        return ', '.join(radicals)
    
class Pronunciation(models.Model):
    TYPE_ON_YOMI = 'on-yomi'
    TYPE_KUN_YOMI = 'kun-yomi'
    TYPE_CHOICES = (
        (TYPE_ON_YOMI, TYPE_ON_YOMI),
        (TYPE_KUN_YOMI, TYPE_KUN_YOMI),
    )
    kanji               = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    type                = models.CharField(max_length=10, choices=TYPE_CHOICES)
    pronunciation       = models.CharField(max_length=10)
    
    

    
class Word(models.Model):
    concept                 = models.OneToOneField(LearnableConcept, on_delete=models.CASCADE)
    word                    = models.CharField(max_length=50)
    kanji_set               = models.ManyToManyField(Kanji, blank=True)
    definition              = models.TextField()
    pronunciation           = models.CharField(max_length=50, blank=True, null=True)
    pronunciation_array     = models.TextField(default='[]')
    is_proper_noun          = models.BooleanField(default=False)
    popularity              = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['popularity']
    
    def kanji_set_string(self):
        # mostly used for verifying word associations are OK
        response = []
        for oKanji in self.kanji_set.all():
            response.append(oKanji.character)
        return ', '.join(response)
            
