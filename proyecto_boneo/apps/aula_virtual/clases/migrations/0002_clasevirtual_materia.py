# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0001_initial'),
        ('planes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasevirtual',
            name='materia',
            field=models.ForeignKey(to='planes.Materia', related_name='clases_virtuales'),
        ),
    ]
