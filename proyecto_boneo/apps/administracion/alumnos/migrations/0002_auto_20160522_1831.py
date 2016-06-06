# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
        ('alumnos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='usuario',
            field=models.OneToOneField(related_name='responsable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='alumno',
            field=models.ForeignKey(related_name='inscripciones', to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='instancia_cursado',
            field=models.ForeignKey(related_name='inscripciones', to='planes.InstanciaCursado'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='alumno',
            field=models.ForeignKey(related_name='asistencias', to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='division',
            field=models.ForeignKey(related_name='asistentes', to='planes.Division'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='division',
            field=models.ForeignKey(related_name='alumnos', to='planes.Division', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='responsable',
            field=models.ForeignKey(related_name='alumnos', on_delete=django.db.models.deletion.PROTECT, to='alumnos.Responsable'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='usuario',
            field=models.OneToOneField(related_name='alumno', to=settings.AUTH_USER_MODEL),
        ),
    ]
