# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0003_auto_20160209_2157'),
        ('personal', '0002_profesor_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncuentroTutoria',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('resumen', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('anio', models.IntegerField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
                ('profesor', models.ForeignKey(to='personal.Profesor')),
            ],
        ),
        migrations.AddField(
            model_name='encuentrotutoria',
            name='tutoria',
            field=models.ForeignKey(to='tutorias.Tutoria'),
        ),
    ]
