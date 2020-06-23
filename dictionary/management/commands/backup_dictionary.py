from django.core.management.base import BaseCommand
from django.core.management import call_command

# from django.conf import settings


class Command(BaseCommand):
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

        output_path = 'fixtures/dictionary.json'

        # create a backup of all Root, Category, Concept, SourceCollection,
        # AutoImportedFields
        call_command(
            "dumpdata",
            "dictionary.LearnableConcept",
            "dictionary.Radical",
            "dictionary.Kanji",
            "dictionary.Pronunciation",
            "dictionary.Word",
            indent=4,
            output=output_path,
        )