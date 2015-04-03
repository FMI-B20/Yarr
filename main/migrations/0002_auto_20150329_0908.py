# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='description',
        ),
        migrations.RemoveField(
            model_name='place',
            name='smoking',
        ),
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='location_type',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
    ]
