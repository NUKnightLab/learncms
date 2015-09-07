# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learncms', '0017_auto_20150823_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capsuleunit',
            name='image',
            field=filebrowser.fields.FileBrowseField(verbose_name='Image', blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(unique=True, help_text="Don't edit this, let it be automatically assigned. Must be unique. If you do edit, you need to edit all lesson-ref slugs referring to this."),
        ),
    ]
