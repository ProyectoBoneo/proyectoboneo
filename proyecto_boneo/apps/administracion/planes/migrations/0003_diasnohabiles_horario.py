# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0002_auto_20160207_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiasNoHabiles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('anio_cursado', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('dia', models.IntegerField()),
                ('hora', models.TimeField()),
                ('instancia_cursado', models.ForeignKey(to='planes.InstanciaCursado')),
            ],
        ),
    ]
