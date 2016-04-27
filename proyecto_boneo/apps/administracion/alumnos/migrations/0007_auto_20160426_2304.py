# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0005_auto_20160419_0212'),
        ('alumnos', '0006_auto_20160420_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='clase_real',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='division',
            field=models.ForeignKey(related_name='asistentes', to='planes.Division', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.datetime.today()),
            preserve_default=False,
        ),
    ]
