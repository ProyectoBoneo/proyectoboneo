# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planes', '0001_initial'),
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='solicitante',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, related_name='solicitante'),
        ),
        migrations.AddField(
            model_name='material',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planes.Materia'),
        ),
    ]
