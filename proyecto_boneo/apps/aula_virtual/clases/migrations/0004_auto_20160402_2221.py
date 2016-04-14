# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0003_auto_20160402_0519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejerciciovirtualmultiplechoice',
            name='orden_prioridad',
        ),
        migrations.RemoveField(
            model_name='ejerciciovirtualtexto',
            name='orden_prioridad',
        ),
        migrations.AddField(
            model_name='ejerciciovirtual',
            name='orden_prioridad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
