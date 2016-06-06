# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('asunto', models.CharField(max_length=150)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fecha_leido', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DestinatarioComunicado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_leido', models.DateTimeField(null=True, blank=True)),
                ('comunicado', models.ForeignKey(to='comunicados.Comunicado')),
            ],
        ),
    ]
