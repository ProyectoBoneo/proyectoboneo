# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0006_auto_20160405_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuestaejerciciovirtual',
            name='clase_virtual',
            field=models.ForeignKey(to='clases.ClaseVirtual', related_name='respuestas'),
        ),
    ]
