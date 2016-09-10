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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('archivo', models.FileField(null=True, upload_to=proyecto_boneo.apps.aula_virtual.biblioteca.models.material_location, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolicitudMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('motivo_rechazo', models.TextField(null=True, blank=True)),
                ('aceptada', models.BooleanField(default=False)),
                ('pendiente_de_respuesta', models.BooleanField(default=True)),
                ('material', models.ForeignKey(default=None, to='biblioteca.Material', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
