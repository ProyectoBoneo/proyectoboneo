# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField(unique=True)),
                ('domicilio', models.CharField(max_length=150)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
                ('legajo', models.BigIntegerField(unique=True)),
                ('_promedio', models.FloatField(blank=True, null=True)),
                ('last_promedio_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('asistio', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InscripcionAlumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_promedio', models.FloatField(blank=True, null=True)),
                ('last_promedio_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField(unique=True)),
                ('domicilio', models.CharField(max_length=150)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
