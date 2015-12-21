from django.core.management.commands.loaddata import Command as LoadDataCommand
from django.core import serializers
from learncms import models

from django.contrib.auth.models import User
from django.utils import timezone


class Command(LoadDataCommand):
    help = '''Counterpart to our custom dumpdata... name explicitly chosen to mask the Django `loaddata`
    command which doesn't play well with the `reversion` plugin'''


    def add_arguments(self, parser):
        parser.add_argument('args', metavar='fixture', nargs='+',
            help='Fixture labels are not used with this version of loaddata.')

    def handle(self, *fixture_labels, **options):

        if (options.get('app_label') != 'learncms'):
            return super().handle(*fixture_labels, **options)

        if fixture_labels:
            print("the custom loaddata command for learncms doesn't use fixtures so assuming this is being called by migrate and doing nothing")
        return

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
