# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0004_asistencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='asistio',
            field=models.BooleanField(default=False),
        ),
    ]
