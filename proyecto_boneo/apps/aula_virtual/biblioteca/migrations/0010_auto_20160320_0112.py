# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0009_solicitudmaterial_pendiente_de_respuesta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudmaterial',
            name='material',
        ),
        migrations.RemoveField(
            model_name='solicitudmaterial',
            name='solicitante',
        ),
        migrations.DeleteModel(
            name='SolicitudMaterial',
        ),
    ]
