# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0006_lesson_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapsuleUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='capsules')),
                ('content', models.TextField(blank=True)),
            ],
        ),
    ]
