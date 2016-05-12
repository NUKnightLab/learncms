"""Supercede Django dump data to avoid problems with versioning and users. Most appropriate for dumping data for a local developer DB.
   Don't forget that you'll also probably want to handle user uploaded images... (on production in ~/learn-media unless core.settings.prd changes)


"""
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from learncms import models


class Command(BaseCommand):
    help = 'Dumps data from the database without the fiddly bits of versions and concurrency...'


    def add_arguments(self, parser):
        pass
        # parser.add_argument('--indent', default=None, dest='indent', type=int,
        #     help='Specifies the indent level to use when pretty-printing output.')

    def handle(self, *fixture_labels, **options):
        with open("learncms/data/lessons.json","w") as o:
            lessons = serializers.serialize('json', models.Lesson.objects.all(),fields=('title','slug','banner_image','status','reference_blurb','content'), indent=2, stream=o)
        with open("learncms/data/zimages.json","w") as o:
            zimages = serializers.serialize('json', models.ZoomingImage.objects.all(), indent=2, stream=o)
        with open("learncms/data/capsules.json","w") as o:
            capsules = serializers.serialize('json', models.CapsuleUnit.objects.all(), fields=('title','slug','image','content'), indent=2, stream=o)
        with open("learncms/data/terms.json","w") as o:
            terms = serializers.serialize('json', models.GlossaryTerm.objects.all(), indent=2, stream=o)
