# Generated by Django 2.0.7 on 2018-07-16 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personal', '0001_initial'),
        ('alumnos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncuentroTutoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('resumen', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnos.Alumno')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Profesor')),
            ],
        ),
        migrations.AddField(
            model_name='encuentrotutoria',
            name='tutoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorias.Tutoria'),
        ),
    ]
