# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150526_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
