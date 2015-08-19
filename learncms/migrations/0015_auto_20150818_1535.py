# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0014_glossaryterm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossaryterm',
            options={'ordering': ['lemma']},
        ),
        migrations.AlterField(
            model_name='glossaryterm',
            name='definition',
            field=models.TextField(help_text="The definition of the term. Don't use markup."),
        ),
    ]
