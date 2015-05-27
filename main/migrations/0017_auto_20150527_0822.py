# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommandationhistory',
            name='location_lat',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommandationhistory',
            name='location_lon',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommandationhistory',
            name='radius',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
