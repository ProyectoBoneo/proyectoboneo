# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0007_auto_20160210_2347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudmaterial',
            old_name='motivo',
            new_name='motivo_rechazo',
        ),
    ]
