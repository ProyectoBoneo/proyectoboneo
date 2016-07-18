# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0005_auto_20160605_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='legajo',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='dni',
            field=models.BigIntegerField(unique=True),
        ),
    ]
