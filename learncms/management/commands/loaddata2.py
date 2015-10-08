from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.loaddata import Command as LoadDataCommand
from django.contrib.auth.models import User
import warnings
from django.core import serializers
import os
from django.db import (
    DEFAULT_DB_ALIAS, DatabaseError, IntegrityError, connections, router,
    transaction,
)
from django.utils.encoding import force_text

from concurrency.api import disable_concurrency

class Command(LoadDataCommand):
    help = 'Installs the named fixture(s) in the database.'
    missing_args_message = ("No database fixture specified. Please provide the "
                            "path of at least one fixture in the command line.")



    def load_label(self, fixture_label):

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) == 0:
            raise Exception("You must create at least one superuser before running this command")

        creator = superusers[0]

        # most of below is copied from core load_label command because it's not factored
        # for the kind of monkey business we want to do.
        # added code is marked...
        for fixture_file, fixture_dir, fixture_name in self.find_fixtures(fixture_label):
            _, ser_fmt, cmp_fmt = self.parse_name(os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]
            fixture = open_method(fixture_file, mode)
            try:
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write("Installing %s fixture '%s' from %s." %
                        (ser_fmt, fixture_name, humanize(fixture_dir)))

                objects = serializers.deserialize(ser_fmt, fixture,
                    using=self.using, ignorenonexistent=self.ignore)

                for obj in objects:
                    objects_in_fixture += 1
                    if router.allow_migrate_model(self.using, obj.object.__class__):
                        loaded_objects_in_fixture += 1
                        self.models.add(obj.object.__class__)
                        try:
                            
                            obj.save(using=self.using)
                        except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': force_text(e)
                            },)
                            raise

                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = ("Problem installing fixture '%s': %s" % (fixture_file, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture_name,
                    RuntimeWarning
                )

def adjust_object(object, superuser):
    if hasattr(object,'version'):
        object.version = None
    if hasattr(object,'updated_at'):
        object.updated_at = None
    if hasattr(object,'updated_by'):
        object.updated_by = None
    if hasattr(object,'created_at'):
        object.created_at = None
    if hasattr(object,'created_by'):
        object.created_by = superuser
