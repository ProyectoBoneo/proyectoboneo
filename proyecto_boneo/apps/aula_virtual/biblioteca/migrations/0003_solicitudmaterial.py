# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0002_auto_20160207_2008'),
        ('biblioteca', '0002_material_materia'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('motivo', models.TextField(null=True, blank=True)),
                ('aceptada', models.BooleanField()),
                ('materia', models.ForeignKey(to='planes.Materia', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
