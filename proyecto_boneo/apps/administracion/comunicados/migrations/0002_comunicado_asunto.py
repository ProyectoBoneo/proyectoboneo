# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comunicados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comunicado',
            name='asunto',
            field=models.TextField(blank=True, default='Mensaje Nuevo', null=True),
        ),
    ]
