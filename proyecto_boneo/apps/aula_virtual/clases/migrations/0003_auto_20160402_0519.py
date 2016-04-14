# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clases', '0002_auto_20150927_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='EjercicioVirtual',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('titulo', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='ejerciciovirtualmultiplechoice',
            name='clase_virtual',
        ),
        migrations.RemoveField(
            model_name='ejerciciovirtualmultiplechoice',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ejerciciovirtualtexto',
            name='clase_virtual',
        ),
        migrations.RemoveField(
            model_name='ejerciciovirtualtexto',
            name='id',
        ),
        migrations.AddField(
            model_name='clasevirtual',
            name='nombre',
            field=models.CharField(default='Clase', max_length=30),
        ),
        migrations.AddField(
            model_name='ejerciciovirtualmultiplechoice',
            name='orden_prioridad',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ejerciciovirtualtexto',
            name='orden_prioridad',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ejerciciovirtual',
            name='clase_virtual',
            field=models.ForeignKey(to='clases.ClaseVirtual', related_name='ejercicios'),
        ),
        migrations.AddField(
            model_name='ejerciciovirtualmultiplechoice',
            name='ejerciciovirtual_ptr',
            field=models.OneToOneField(to='clases.EjercicioVirtual', serialize=False, parent_link=True, primary_key=True, default=1, auto_created=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ejerciciovirtualtexto',
            name='ejerciciovirtual_ptr',
            field=models.OneToOneField(to='clases.EjercicioVirtual', serialize=False, parent_link=True, primary_key=True, default='1', auto_created=True),
            preserve_default=False,
        ),
    ]
