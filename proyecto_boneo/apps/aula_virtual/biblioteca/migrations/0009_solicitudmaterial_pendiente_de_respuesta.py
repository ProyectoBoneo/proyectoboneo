# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0008_auto_20160313_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='pendiente_de_respuesta',
            field=models.BooleanField(default=True),
        ),
    ]
