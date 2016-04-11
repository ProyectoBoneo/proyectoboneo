# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20160322_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioboneo',
            name='is_alumno',
            field=models.BooleanField(verbose_name='alumno', default=False, help_text='Designates whether this user should be treated as alumno.'),
        ),
        migrations.AlterField(
            model_name='usuarioboneo',
            name='is_profesor',
            field=models.BooleanField(verbose_name='profesor', default=False, help_text='Designates whether this user should be treated as profesor.'),
        ),
    ]
