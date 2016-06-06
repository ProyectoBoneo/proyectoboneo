# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
        ('biblioteca', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='solicitante',
            field=models.ForeignKey(default=None, related_name='solicitante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planes.Materia'),
        ),
    ]
