# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comunicados', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            field=models.ManyToManyField(through='comunicados.DestinatarioComunicado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comunicado',
            name='emisor',
            field=models.ForeignKey(related_name='usuario_emisor', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
