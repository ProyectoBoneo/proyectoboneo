# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tutorias', '0002_auto_20160327_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentrotutoria',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2016, 9, 10, 15, 10, 26, 388334, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='encuentrotutoria',
            name='fecha',
            field=models.DateField(),
        ),
    ]
