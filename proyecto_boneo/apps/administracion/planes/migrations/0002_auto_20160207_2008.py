# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanciacursado',
            name='division',
            field=models.ForeignKey(to='planes.Division', related_name='instancias_cursado'),
        ),
        migrations.AlterField(
            model_name='instanciacursado',
            name='materia',
            field=models.ForeignKey(to='planes.Materia', related_name='instancias_cursado'),
        ),
    ]
