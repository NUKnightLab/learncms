# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0015_auto_20150818_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='banner_image',
            field=filebrowser.fields.FileBrowseField(verbose_name='Banner Image', max_length=200, blank=True),
        ),
    ]
