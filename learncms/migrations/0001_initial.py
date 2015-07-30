# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('position', models.IntegerField(help_text='Index of this block among all blocks of a lesson')),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('banner_image', models.ImageField(upload_to='lessons')),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZoomingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to='z_images')),
                ('lesson', models.ForeignKey(to='learncms.Lesson')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='lesson',
            field=models.ForeignKey(to='learncms.Lesson'),
        ),
    ]
