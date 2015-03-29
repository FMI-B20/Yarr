# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_locationtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='location_type',
        ),
        migrations.AddField(
            model_name='place',
            name='location_types',
            field=models.ManyToManyField(to='main.LocationType'),
            preserve_default=True,
        ),
    ]
