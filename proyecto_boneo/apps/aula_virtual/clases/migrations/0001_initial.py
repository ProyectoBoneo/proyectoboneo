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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioVirtualMultipleChoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ayuda', models.TextField(null=True, blank=True)),
                ('pregunta', models.CharField(max_length=100)),
                ('explicacion', models.TextField(null=True, blank=True)),
                ('clase_virtual', models.ForeignKey(related_name='ejercicios_multiple_choice', to='clases.ClaseVirtual')),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioVirtualTexto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ayuda', models.TextField(null=True, blank=True)),
                ('consigna', models.CharField(max_length=100)),
                ('clase_virtual', models.ForeignKey(related_name='ejercicios_texto', to='clases.ClaseVirtual')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionEjercicioMultipleChoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('texto', models.CharField(max_length=100)),
                ('opcion_correcta', models.BooleanField(default=False)),
                ('ejercicio', models.ForeignKey(related_name='opciones', to='clases.EjercicioVirtualMultipleChoice')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtualMultipleChoice',
            fields=[
                ('respuestaejerciciovirtual_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='clases.RespuestaEjercicioVirtual', serialize=False, parent_link=True)),
            ],
            bases=('clases.respuestaejerciciovirtual',),
        ),
        migrations.CreateModel(
            name='RespuestaEjercicioVirtualTexto',
            fields=[
                ('respuestaejerciciovirtual_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='clases.RespuestaEjercicioVirtual', serialize=False, parent_link=True)),
                ('texto', models.TextField()),
            ],
            bases=('clases.respuestaejerciciovirtual',),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtual',
            name='alumno',
            field=models.ForeignKey(related_name='+', to='alumnos.Alumno'),
        ),
    ]
