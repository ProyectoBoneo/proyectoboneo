# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='responsable'),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='alumno',
            field=models.ForeignKey(to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='instancia_cursado',
            field=models.ForeignKey(to='planes.InstanciaCursado'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='division',
            field=models.ForeignKey(to='planes.Division'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='responsable',
            field=models.ForeignKey(to='alumnos.Responsable', on_delete=django.db.models.deletion.PROTECT, related_name='alumnos'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='alumno'),
        ),
    ]
