from django.core.management.base import BaseCommand
from django.core.management import call_command

from dictionary import models

# from django.conf import settings


class Command(BaseCommand):
    ''' WARNING! This will destroy the progress for all users!!!
    '''
    help = "Backs up the dictionary."

    def print_out(self, *args):
        """ A wrapper for self.stdout.write() that converts anything into a string """
        strings = []
        for arg in args:
            strings.append(str(arg))
        self.stdout.write(",".join(strings))

    def print_err(self, *args):
        """ A wrapper for self.stderr.write() that converts anything into a string """
        strings = []
        for arg in args:
            strings.append(str(arg))
        self.stderr.write(",".join(strings))

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        fixture_path = 'fixtures/dictionary.json'

        models.Pronunciation.objects.all().delete()
        models.Radical.objects.all().delete()
        models.Word.objects.all().delete()
        models.Kanji.objects.all().delete()
        models.LearnableConcept.objects.all().delete()

        call_command(
            "loaddata", fixture_path,
        )