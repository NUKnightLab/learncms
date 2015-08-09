# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0010_auto_20150807_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalimage',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
