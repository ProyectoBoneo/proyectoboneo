# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
        ('clases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasevirtual',
            name='materia',
            field=models.ForeignKey(related_name='clases_virtuales', to='planes.Materia'),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtualtexto',
            name='ejercicio',
            field=models.ForeignKey(related_name='respuestas', to='clases.EjercicioVirtualTexto'),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtualmultiplechoice',
            name='ejercicio',
            field=models.ForeignKey(related_name='respuestas', to='clases.EjercicioVirtualMultipleChoice'),
        ),
        migrations.AddField(
            model_name='respuestaejerciciovirtualmultiplechoice',
            name='opcion_seleccionada',
            field=models.ForeignKey(related_name='+', to='clases.OpcionEjercicioMultipleChoice'),
        ),
        migrations.AddField(
            model_name='opcionejerciciomultiplechoice',
            name='ejercicio',
            field=models.ForeignKey(related_name='opciones', to='clases.EjercicioVirtualMultipleChoice'),
        ),
    ]
