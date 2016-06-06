# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_auto_20160522_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='_promedio',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumno',
            name='last_promedio_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 5, 20, 35, 13, 469696)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='_promedio',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='last_promedio_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 5, 20, 35, 27, 893293)),
            preserve_default=False,
        ),
    ]
