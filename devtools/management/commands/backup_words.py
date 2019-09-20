import json

from django.core.management.base import BaseCommand, CommandError

from devtools import models

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

#     def add_arguments(self, parser):
#         parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        
#         word                    = models.CharField(max_length=50)
#         characters              = models.ManyToManyField(Character)
#         definition              = models.TextField()
#         pronunciation           = models.CharField(max_length=50, blank=True, null=True)
#         pronunciation_array     = models.TextField(default='[]')
#         is_proper_noun          = models.BooleanField(default=False)
#         popularity              = models.IntegerField(null=True, blank=True)
        word_list = []
        for oWord in models.Words.objects.all():
            entry = {
                'word' : oWord.word,
                'popularity' : oWord.word_ranking,
                'definition' : oWord.definition,
                'is_proper_noun' : oWord.proper_noun,
                'pronunciation' : oWord.get_pronunciation(),
            }
            pronunciation_array = []
            for oFurigana in oWord.wordfurigana_set.all().order_by('position'):
                pronunciation_array.append(oFurigana.furigana)
                
            entry['pronunciation_array'] = pronunciation_array
            word_list.append(entry)
            
        with open('_data/word_list.json', 'w', encoding='utf-8') as f:
            json.dump(word_list, f, ensure_ascii=False, indent=4)

            