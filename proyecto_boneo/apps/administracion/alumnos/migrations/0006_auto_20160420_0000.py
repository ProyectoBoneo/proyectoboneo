# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0005_asistencia_asistio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asistencia',
            old_name='claseReal',
            new_name='clase_real',
        ),
    ]
