# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150329_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='phone_number1',
            field=models.TextField(null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'")]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='phone_number2',
            field=models.TextField(null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'")]),
            preserve_default=True,
        ),
    ]
