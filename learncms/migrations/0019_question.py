# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0018_auto_20150907_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('question', models.TextField(help_text="The definition of the term. Don't use markup.")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('page', models.CharField(blank=True, help_text='The slug of the lesson page where the question was asked', max_length=50)),
                ('step', models.CharField(blank=True, help_text='As much as possible about where in the page the asker was when asking.', max_length=100)),
            ],
        ),
    ]
