# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0004_auto_20160209_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='justificacion',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
