# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0003_auto_20150730_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='reference_blurb',
            field=models.CharField(max_length=500, help_text='The text which appears when a reference to this lesson is included in some other.', blank=True),
        ),
    ]
