# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0003_diasnohabiles_horario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseReal',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('semana_ano', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='horario',
            old_name='dia',
            new_name='dia_semana',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='hora',
        ),
        migrations.AddField(
            model_name='horario',
            name='hora_fin',
            field=models.TimeField(default='12:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='horario',
            name='hora_inicio',
            field=models.TimeField(default='12:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='horario',
            name='instancia_cursado',
            field=models.ForeignKey(to='planes.InstanciaCursado', related_name='horarios'),
        ),
        migrations.AddField(
            model_name='clasereal',
            name='horario',
            field=models.ForeignKey(to='planes.Horario', related_name='clases'),
        ),
    ]
