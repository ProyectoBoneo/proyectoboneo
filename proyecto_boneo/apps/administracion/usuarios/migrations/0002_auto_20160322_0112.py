# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioboneo',
            name='is_alumno',
            field=models.BooleanField(help_text='Designates whether this user should be treated as alumno.', verbose_name='alumno', default=True),
        ),
        migrations.AddField(
            model_name='usuarioboneo',
            name='is_profesor',
            field=models.BooleanField(help_text='Designates whether this user should be treated as profesor.', verbose_name='profesor', default=True),
        ),
    ]
