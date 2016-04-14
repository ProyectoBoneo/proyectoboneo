# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0005_remove_ejerciciovirtual_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestaejerciciovirtual',
            name='clase_virtual',
            field=models.ForeignKey(default=1, to='clases.ClaseVirtual', related_name='+'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtual',
            name='es_correcta',
            field=models.NullBooleanField(default=None),
        ),
    ]
