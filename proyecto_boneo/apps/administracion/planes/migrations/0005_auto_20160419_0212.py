# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0004_auto_20160417_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clasereal',
            name='semana_ano',
        ),
        migrations.AddField(
            model_name='clasereal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 5, 11, 57, 527236, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clasereal',
            name='hora_fin',
            field=models.TimeField(default='12:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clasereal',
            name='hora_inicio',
            field=models.TimeField(default='10:00'),
            preserve_default=False,
        ),
    ]
