# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0003_auto_20160605_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='_promedio',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='last_promedio_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
