# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncuentroTutoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('resumen', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
