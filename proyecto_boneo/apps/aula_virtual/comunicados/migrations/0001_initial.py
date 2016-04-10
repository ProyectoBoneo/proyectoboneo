# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fecha_leido', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DestinatarioComunicado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_leido', models.DateTimeField(null=True, blank=True)),
                ('comunicado', models.ForeignKey(to='comunicados.Comunicado')),
                ('destinatario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comunicado',
            name='destinatarios',
            field=models.ManyToManyField(through='comunicados.DestinatarioComunicado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comunicado',
            name='emisor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_emisor'),
        ),
    ]
