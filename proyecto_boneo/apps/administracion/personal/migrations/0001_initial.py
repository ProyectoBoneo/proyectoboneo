# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('dni', models.BigIntegerField()),
                ('domicilio', models.CharField(max_length=150)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
                ('legajo', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
