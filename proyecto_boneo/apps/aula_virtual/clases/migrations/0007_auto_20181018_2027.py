# Generated by Django 2.0.7 on 2018-10-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0006_auto_20181018_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clasevirtual',
            options={'ordering': ('fecha', 'materia', 'tipo')},
        ),
        migrations.RemoveField(
            model_name='clasevirtual',
            name='publicado',
        ),
        migrations.AlterField(
            model_name='clasevirtual',
            name='fecha',
            field=models.DateField(),
        ),
    ]
