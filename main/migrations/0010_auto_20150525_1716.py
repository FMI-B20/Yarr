# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150523_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image_url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
