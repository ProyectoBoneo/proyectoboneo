# Generated by Django 2.0.7 on 2018-07-16 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('planes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudmaterial',
            name='solicitante',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='solicitante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planes.Materia'),
        ),
    ]