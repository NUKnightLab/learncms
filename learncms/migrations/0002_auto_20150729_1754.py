# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zoomingimage',
            name='lesson',
        ),
        migrations.AddField(
            model_name='zoomingimage',
            name='lessons',
            field=models.ManyToManyField(to='learncms.Lesson'),
        ),
    ]
