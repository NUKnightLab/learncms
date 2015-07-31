# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0004_auto_20150730_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='reference_blurb',
            field=models.CharField(help_text="The text which appears when a reference to this lesson is included in some other. Don't use markup.", blank=True, max_length=500),
        ),
    ]
