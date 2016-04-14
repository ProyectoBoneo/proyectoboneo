# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0007_auto_20160410_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuestaejerciciovirtual',
            name='alumno',
            field=models.ForeignKey(related_name='respuestas', to='alumnos.Alumno'),
        ),
    ]
