# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import concurrency.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0011_auto_20150809_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='version',
            field=concurrency.fields.IntegerVersionField(help_text='record revision number', default=0),
        ),
    ]
