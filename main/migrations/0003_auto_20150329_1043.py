# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150329_0908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='cuisine',
        ),
        migrations.AddField(
            model_name='place',
            name='cuisines',
            field=models.ManyToManyField(to='main.Cuisine'),
            preserve_default=True,
        ),
    ]
