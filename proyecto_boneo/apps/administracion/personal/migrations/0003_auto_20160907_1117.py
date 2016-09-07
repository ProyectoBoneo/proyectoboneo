# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_profesor_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesor',
            name='dni',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='legajo',
            field=models.BigIntegerField(unique=True),
        ),
    ]
