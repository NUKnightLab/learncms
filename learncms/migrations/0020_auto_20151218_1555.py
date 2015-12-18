# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0019_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='step_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='email',
            field=models.EmailField(blank=True, max_length=254, help_text='Optionally, an email address of the asker.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(help_text='The question submitted.'),
        ),
    ]
