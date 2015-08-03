# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learncms', '0006_lesson_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 18, 22, 3, 682726, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='creator'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 18, 22, 7, 817958, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='updater'),
        ),
    ]
