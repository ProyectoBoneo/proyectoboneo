# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('anio', models.IntegerField()),
                ('letra', models.CharField(null=True, blank=True, max_length=1)),
                ('activa', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['anio', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='InstanciaCursado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('anio_cursado', models.IntegerField()),
                ('division', models.ForeignKey(to='planes.Division')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
            field=models.ForeignKey(to='planes.Materia'),
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='profesor_titular',
            field=models.ForeignKey(null=True, blank=True, to='personal.Profesor'),
        ),
    ]
