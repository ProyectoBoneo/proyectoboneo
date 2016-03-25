# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biblioteca', '0010_auto_20160320_0112'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('motivo_rechazo', models.TextField(null=True, blank=True)),
                ('aceptada', models.BooleanField(default=False)),
                ('pendiente_de_respuesta', models.BooleanField(default=True)),
                ('material', models.ForeignKey(null=True, default=None, blank=True, to='biblioteca.Material')),
                ('solicitante', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, related_name='solicitante')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
