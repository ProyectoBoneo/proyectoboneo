# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0008_auto_20160910_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estadia',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
                ('responsable', models.ForeignKey(to='alumnos.Responsable')),
            ],
        ),
    ]
