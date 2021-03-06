# Generated by Django 2.0.7 on 2018-07-16 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('planes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumnos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='responsable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='inscripcionalumno',
            name='instancia_cursado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='planes.InstanciaCursado'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='alumnos.Alumno'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistentes', to='planes.Division'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alumnos', to='planes.Division'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alumnos', to='alumnos.Responsable'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='alumno', to=settings.AUTH_USER_MODEL),
        ),
    ]
