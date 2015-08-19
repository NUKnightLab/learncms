# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0013_capsuleunit_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryTerm',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('lemma', models.CharField(max_length=50, help_text='The canonical form of the word or phrase being defined.')),
                ('definition', models.TextField(help_text='The definition of the term.')),
            ],
        ),
    ]
