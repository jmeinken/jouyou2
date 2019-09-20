import json

from django.core.management.base import BaseCommand, CommandError

from devtools import loaders
from dictionary import models


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

#     def add_arguments(self, parser):
#         parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        
        self.clear_database()
        self.load_kanji()
        self.load_radicals()
        self.load_radical_associations()   
        self.associate_radicals_with_identical_kanji() 

        self.load_words()
        
    def associate_radicals_with_identical_kanji(self):
        for oRad in models.Radical.objects.all():
            oKanji = models.Kanji.objects.filter(character=oRad.character).first()
            if oKanji:
                if not oRad.meaning:
                    oRad.meaning = oKanji.meaning
                oRad.identical_kanji = oKanji
                oRad.save()
        
    def load_words(self):
        for entry in loaders.get_words():
            oConcept = models.LearnableConcept(type=models.LearnableConcept.TYPE_WORD)
            oConcept.save()
            oWord = models.Word(
                concept=oConcept,
                word=entry['word'],
                definition=entry['definition'],
                pronunciation=entry['pronunciation'],
                pronunciation_array=json.dumps(entry['pronunciation_array']),
                is_proper_noun=entry['is_proper_noun'],
                popularity=entry['popularity']
            )
            oWord.save()
            for char in oWord.word:
                oKanji = models.Kanji.objects.filter(character=char).first()
                if oKanji:
                    oWord.kanji_set.add(oKanji)

    def load_radicals(self):
        entries = loaders.get_radical_meanings()
        for entry in entries:
            oRad, created = models.Radical.objects.get_or_create(character=entry['radical'])
            if created:
                oRad.stroke_count = entry['stroke_count']
                oRad.meaning = entry['meaning']
            oRad.save()
            
        
    def load_radical_associations(self):
        generator = loaders.radical_generator()
        for entry in generator:
            oKanji = models.Kanji.objects.filter(character=entry['kanji']).first()
            if oKanji:
                for radical in entry['radicals']:
                    oRad, created = models.Radical.objects.get_or_create(character=radical)
                    oKanji.radicals.add(oRad)

        
    def clear_database(self):
        for oConcept in models.LearnableConcept.objects.all():
            oConcept.delete()
        for oRadical  in models.Radical.objects.all():
            oRadical.delete()

            
    def load_kanji(self):
        generator = loaders.kanjidic_generator()
        count = 0
        for entry in generator:
            if not 'grade' in entry or not entry['grade']:
                continue
            # some advanced kanji aren't able to be read for some reason
            if entry['kanji'] == '\u25A0':
                continue
            oConcept = models.LearnableConcept(type=models.LearnableConcept.TYPE_CHAR)
            oConcept.save()
            oKanji = models.Kanji(
                concept=oConcept,
                character=entry['kanji'],
                grade=entry['grade'],
                stroke_count=entry['stroke_count'],
                popularity=entry['popularity'] if 'popularity' in entry else None,
                jlpt_level=entry['jlpt_level'] if 'jlpt_level' in entry else None,
                meaning=', '.join(entry['meanings']),
            )
            if entry['on_yomis']:
                oKanji.main_pronunciation = entry['on_yomis'][0]
            oKanji.save()
            for on_yomi in entry['on_yomis']:
                oPron = models.Pronunciation(
                    kanji = oKanji,
                    type = models.Pronunciation.TYPE_ON_YOMI,
                    pronunciation = on_yomi
                )
                oPron.save()
            for kun_yomi in entry['kun_yomis']:
                oPron = models.Pronunciation(
                    kanji = oKanji,
                    type = models.Pronunciation.TYPE_KUN_YOMI,
                    pronunciation = kun_yomi
                )
                oPron.save()
            count += 1
            print(count)
