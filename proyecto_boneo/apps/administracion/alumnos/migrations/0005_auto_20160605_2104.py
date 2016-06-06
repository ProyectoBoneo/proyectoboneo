# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0004_auto_20160605_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcionalumno',
            name='_promedio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inscripcionalumno',
            name='last_promedio_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
