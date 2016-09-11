# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comunicados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinatariocomunicado',
            name='destinatario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comunicado',
            name='destinatarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='comunicados.DestinatarioComunicado'),
        ),
        migrations.AddField(
            model_name='comunicado',
            name='emisor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='usuario_emisor', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
