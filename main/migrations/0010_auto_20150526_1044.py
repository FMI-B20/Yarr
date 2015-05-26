# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_auto_20150523_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommandationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('location_lat', models.FloatField()),
                ('location_lon', models.FloatField()),
                ('radius', models.FloatField()),
                ('cuisines', models.ManyToManyField(to='main.Cuisine')),
                ('location_types', models.ManyToManyField(to='main.LocationType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='place',
            name='image_url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
