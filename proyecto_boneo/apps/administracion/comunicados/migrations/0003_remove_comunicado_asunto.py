# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comunicados', '0002_comunicado_asunto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comunicado',
            name='asunto',
        ),
    ]
