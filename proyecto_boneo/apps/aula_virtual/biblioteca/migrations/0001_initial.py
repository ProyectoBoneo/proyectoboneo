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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('archivo', models.FileField(upload_to=proyecto_boneo.apps.aula_virtual.biblioteca.models.material_location, null=True, blank=True)),
            ],
        ),
    ]
