# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
        ('planes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='materia',
            field=models.ForeignKey(to='planes.Materia', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
