# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseReal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DiasNoHabiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('anio_cursado', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('anio', models.IntegerField()),
                ('letra', models.CharField(max_length=1, null=True, blank=True)),
                ('activa', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['anio', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dia_semana', models.IntegerField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InstanciaCursado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('anio_cursado', models.IntegerField()),
                ('division', models.ForeignKey(related_name='instancias_cursado', to='planes.Division')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('anio', models.IntegerField()),
            ],
            options={
                'ordering': ['anio', 'descripcion'],
            },
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='materia',
            field=models.ForeignKey(related_name='instancias_cursado', to='planes.Materia'),
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='profesor_titular',
            field=models.ForeignKey(to='personal.Profesor', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='horario',
            name='instancia_cursado',
            field=models.ForeignKey(related_name='horarios', to='planes.InstanciaCursado'),
        ),
        migrations.AddField(
            model_name='clasereal',
            name='horario',
            field=models.ForeignKey(related_name='clases', to='planes.Horario'),
        ),
    ]
