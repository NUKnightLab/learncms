# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50, help_text='The label which will be shown on the unit.')),
                ('image', models.ImageField(upload_to='linkrefs')),
                ('slug', models.SlugField(help_text="Don't edit this, let it be automatically assigned. Must be unique.", unique=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='capsuleunit',
            name='content',
            field=models.TextField(blank=True, help_text='HTML is OK'),
        ),
        migrations.AlterField(
            model_name='capsuleunit',
            name='slug',
            field=models.SlugField(help_text="Don't edit this, let it be automatically assigned. Must be unique.", unique=True),
        ),
        migrations.AlterField(
            model_name='zoomingimage',
            name='image',
            field=models.ImageField(help_text='Upload the full-size version of the image. The system will create the thumbnail.', upload_to='zimages'),
        ),
        migrations.AlterField(
            model_name='zoomingimage',
            name='slug',
            field=models.SlugField(help_text='You choose. Lowercase letters and numbers and - characters only please.', unique=True),
        ),
    ]
