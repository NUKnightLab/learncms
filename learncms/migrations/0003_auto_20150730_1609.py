# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0002_auto_20150729_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='zoomingimage',
            name='lessons',
        ),
        migrations.AddField(
            model_name='lesson',
            name='reference_blurb',
            field=models.TextField(blank=True, help_text='The text which appears when a reference to this lesson is included in some other.'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=models.TextField(blank=True, help_text='The body of the lesson, marked up with web component magic.'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(unique=True, help_text="Don't edit this, let it be automatically assigned. Must be unique."),
        ),
        migrations.AlterField(
            model_name='zoomingimage',
            name='image',
            field=models.ImageField(upload_to='zimages'),
        ),
        migrations.AlterField(
            model_name='zoomingimage',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.DeleteModel(
            name='Block',
        ),
    ]
