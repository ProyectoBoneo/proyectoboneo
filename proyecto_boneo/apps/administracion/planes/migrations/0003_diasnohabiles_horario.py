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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('anio_cursado', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('dia', models.IntegerField()),
                ('hora', models.TimeField()),
                ('instancia_cursado', models.ForeignKey(to='planes.InstanciaCursado')),
            ],
        ),
    ]
