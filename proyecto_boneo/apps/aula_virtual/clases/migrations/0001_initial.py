# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(default='Clase', max_length=30)),
                ('descripcion', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=3, choices=[('nor', 'Clase Virtual'), ('eva', 'Evaluación'), ('esc', 'Evaluación Escrita')])),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('orden_prioridad', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpcionEjercicioMultipleChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.CharField(max_length=100)),
                ('opcion_correcta', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('es_correcta', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoEvaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nota', models.FloatField()),
                ('alumno', models.ForeignKey(related_name='resultados_evaluaciones', to='alumnos.Alumno')),
                ('clase_virtual', models.ForeignKey(related_name='resultados', to='clases.ClaseVirtual')),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioVirtualMultipleChoice',
            fields=[
                ('ejerciciovirtual_ptr', models.OneToOneField(auto_created=True, to='clases.EjercicioVirtual', primary_key=True, serialize=False, parent_link=True)),
                ('ayuda', models.TextField(null=True, blank=True)),
                ('pregunta', models.CharField(max_length=100)),
                ('explicacion', models.TextField(null=True, blank=True)),
            ],
            bases=('clases.ejerciciovirtual',),
        ),
        migrations.CreateModel(
            name='EjercicioVirtualTexto',
            fields=[
                ('ejerciciovirtual_ptr', models.OneToOneField(auto_created=True, to='clases.EjercicioVirtual', primary_key=True, serialize=False, parent_link=True)),
                ('ayuda', models.TextField(null=True, blank=True)),
                ('consigna', models.CharField(max_length=100)),
            ],
            bases=('clases.ejerciciovirtual',),
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtualMultipleChoice',
            fields=[
                ('respuestaejerciciovirtual_ptr', models.OneToOneField(auto_created=True, to='clases.RespuestaEjercicioVirtual', primary_key=True, serialize=False, parent_link=True)),
            ],
            bases=('clases.respuestaejerciciovirtual',),
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtualTexto',
            fields=[
                ('respuestaejerciciovirtual_ptr', models.OneToOneField(auto_created=True, to='clases.RespuestaEjercicioVirtual', primary_key=True, serialize=False, parent_link=True)),
                ('texto', models.TextField()),
            ],
            bases=('clases.respuestaejerciciovirtual',),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtual',
            name='alumno',
            field=models.ForeignKey(related_name='respuestas', to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtual',
            name='clase_virtual',
            field=models.ForeignKey(related_name='respuestas', to='clases.ClaseVirtual'),
        ),
        migrations.AddField(
            model_name='ejerciciovirtual',
            name='clase_virtual',
            field=models.ForeignKey(related_name='ejercicios', to='clases.ClaseVirtual'),
        ),
    ]
