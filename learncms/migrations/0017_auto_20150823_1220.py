# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0016_auto_20150818_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalimage',
            name='image',
            field=filebrowser.fields.FileBrowseField(verbose_name='Media Library File', max_length=200),
        ),
    ]
