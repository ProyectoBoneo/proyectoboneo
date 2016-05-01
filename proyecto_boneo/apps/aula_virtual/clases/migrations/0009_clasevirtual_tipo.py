# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0008_auto_20160410_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasevirtual',
            name='tipo',
            field=models.CharField(default='nor', max_length=3, choices=[('nor', 'Clase Virtual'), ('eva', 'Evaluación'), ('esc', 'Evaluación Escrita')]),
            preserve_default=False,
        ),
    ]
