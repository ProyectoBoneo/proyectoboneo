# Generated by Django 2.0.7 on 2018-10-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='fecha_fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha_inicio',
            field=models.DateTimeField(),
        ),
    ]
