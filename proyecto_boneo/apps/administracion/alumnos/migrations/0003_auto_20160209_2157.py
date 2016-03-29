# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_auto_20150927_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='division',
            field=models.ForeignKey(to='planes.Division', related_name='alumnos'),
        ),
        migrations.AlterField(
            model_name='inscripcionalumno',
            name='alumno',
            field=models.ForeignKey(to='alumnos.Alumno', related_name='inscripciones'),
        ),
        migrations.AlterField(
            model_name='inscripcionalumno',
            name='instancia_cursado',
            field=models.ForeignKey(to='planes.InstanciaCursado', related_name='inscripciones'),
        ),
    ]
