# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0007_auto_20160426_2304'),
        ('clases', '0009_clasevirtual_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultadoEvaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nota', models.FloatField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno', related_name='resultados_evaluaciones')),
                ('clase_virtual', models.ForeignKey(to='clases.ClaseVirtual', related_name='resultados')),
            ],
        ),
    ]
