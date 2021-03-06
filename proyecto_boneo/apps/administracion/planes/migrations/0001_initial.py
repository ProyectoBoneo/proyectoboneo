# Generated by Django 2.0.7 on 2018-07-16 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField()),
                ('letra', models.CharField(blank=True, max_length=1, null=True)),
                ('activa', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['anio', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.IntegerField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InstanciaCursado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio_cursado', models.IntegerField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instancias_cursado', to='planes.Division')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('anio', models.IntegerField()),
            ],
            options={
                'ordering': ['anio', 'descripcion'],
            },
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instancias_cursado', to='planes.Materia'),
        ),
        migrations.AddField(
            model_name='instanciacursado',
            name='profesor_titular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personal.Profesor'),
        ),
        migrations.AddField(
            model_name='horario',
            name='instancia_cursado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='planes.InstanciaCursado'),
        ),
    ]
