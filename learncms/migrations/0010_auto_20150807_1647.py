# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0009_auto_20150807_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='linkrefs')),
                ('description', models.TextField(blank=True, help_text='Anything that you might want to use to search for this image later.')),
            ],
        ),
        migrations.DeleteModel(
            name='LinkReference',
        ),
    ]
