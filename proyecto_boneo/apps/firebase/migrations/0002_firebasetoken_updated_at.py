# Generated by Django 2.0.7 on 2018-08-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firebase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='firebasetoken',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
