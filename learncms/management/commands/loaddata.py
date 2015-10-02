from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from learncms import models

from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Dumps data from the database without the fiddly bits of versions and concurrency...'


    def add_arguments(self, parser):
        pass
        # parser.add_argument('--indent', default=None, dest='indent', type=int,
        #     help='Specifies the indent level to use when pretty-printing output.')

    def handle(self, *fixture_labels, **options):

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) == 0:
            raise Exception("You must create at least one superuser before running this command")

        creator = superusers[0]
        with open("learncms/fixtures/lessons.json") as o:
                objects = serializers.deserialize('json', o)
                for o in objects:
                    o.object.created_by = creator
                    o.object.created_at = timezone.now()
                    o.object.save()

        with open("learncms/fixtures/zimages.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
        with open("learncms/fixtures/capsules.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
        with open("learncms/fixtures/terms.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
