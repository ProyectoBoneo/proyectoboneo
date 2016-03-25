# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0006_remove_solicitudmaterial_justificacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudmaterial',
            name='materia',
        ),
        migrations.AlterField(
            model_name='solicitudmaterial',
            name='aceptada',
            field=models.BooleanField(default=False),
        ),
    ]
