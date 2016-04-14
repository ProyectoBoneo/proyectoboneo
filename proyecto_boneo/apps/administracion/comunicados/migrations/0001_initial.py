# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('destinatarios', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('emisor', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='usuario_emisor', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
