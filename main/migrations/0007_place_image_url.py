# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150406_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='image_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
