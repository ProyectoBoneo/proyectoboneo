# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0004_auto_20160417_1925'),
        ('alumnos', '0003_auto_20160209_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('alumno', models.ForeignKey(to='alumnos.Alumno', related_name='asistencias')),
                ('claseReal', models.ForeignKey(to='planes.ClaseReal', related_name='asistentes')),
            ],
        ),
    ]
