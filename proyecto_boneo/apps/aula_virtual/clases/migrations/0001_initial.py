# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0006_auto_20160706_2239'),
        ('planes', '0002_auto_20160605_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(default='Clase', max_length=30)),
                ('descripcion', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('nor', 'Clase Virtual'), ('eva', 'Evaluación'), ('esc', 'Evaluación Escrita')], max_length=3)),
                ('materia', models.ForeignKey(to='planes.Materia', related_name='clases_virtuales')),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('tipo_ejercicio', models.CharField(choices=[('txt', 'Texto'), ('mch', 'Multiple Choice')], max_length=3)),
                ('puntaje', models.IntegerField(blank=True, null=True)),
                ('orden_prioridad', models.IntegerField(blank=True, null=True)),
                ('consigna', models.CharField(max_length=100)),
                ('ayuda', models.TextField(blank=True, null=True)),
                ('explicacion', models.TextField(blank=True, null=True)),
                ('clase_virtual', models.ForeignKey(to='clases.ClaseVirtual', related_name='ejercicios')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionEjercicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('texto', models.CharField(max_length=100)),
                ('opcion_correcta', models.BooleanField(default=False)),
                ('ejercicio', models.ForeignKey(to='clases.EjercicioVirtual', related_name='opciones')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('texto', models.TextField(null=True, default=None)),
                ('es_correcta', models.NullBooleanField(default=None)),
                ('alumno', models.ForeignKey(to='alumnos.Alumno', related_name='respuestas')),
                ('clase_virtual', models.ForeignKey(to='clases.ClaseVirtual', related_name='respuestas')),
                ('ejercicio', models.ForeignKey(to='clases.EjercicioVirtual', related_name='respuestas')),
                ('opcion_seleccionada', models.ForeignKey(null=True, to='clases.OpcionEjercicio', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoEvaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nota', models.FloatField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno', related_name='resultados_evaluaciones')),
                ('clase_virtual', models.ForeignKey(to='clases.ClaseVirtual', related_name='resultados')),
            ],
        ),
    ]
