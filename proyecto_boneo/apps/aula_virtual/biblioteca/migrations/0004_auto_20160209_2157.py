# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biblioteca', '0003_solicitudmaterial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='material',
            field=models.ForeignKey(null=True, to='biblioteca.Material', default=None, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudmaterial',
            name='solicitante',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None, related_name='solicitante'),
        ),
    ]
