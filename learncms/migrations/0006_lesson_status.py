# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0005_auto_20150731_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=50),
        ),
    ]
