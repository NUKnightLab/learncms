from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from learncms import models

from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = '''Counterpart to our custom dumpdata... name explicitly chosen to mask the Django `loaddata`
    command which doesn't play well with the `reversion` plugin'''

    def handle(self, *fixture_labels, **options):

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) == 0:
            raise Exception("You must create at least one superuser before running this command")

        creator = superusers[0]
        with open("learncms/data/lessons.json") as o:
                objects = serializers.deserialize('json', o)
                for o in objects:
                    o.object.created_by = creator
                    o.object.created_at = timezone.now()
                    o.object.save()

        with open("learncms/data/zimages.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
        with open("learncms/data/capsules.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
        with open("learncms/data/terms.json") as o:
            for o in serializers.deserialize('json', o):
                o.save()
