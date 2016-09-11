# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import proyecto_boneo.apps.aula_virtual.biblioteca.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('archivo', models.FileField(blank=True, null=True, upload_to=proyecto_boneo.apps.aula_virtual.biblioteca.models.material_location)),
                ('publicado', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolicitudMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('motivo_rechazo', models.TextField(blank=True, null=True)),
                ('aceptada', models.BooleanField(default=False)),
                ('pendiente_de_respuesta', models.BooleanField(default=True)),
                ('material', models.ForeignKey(default=None, to='biblioteca.Material', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
