# Generated by Django 3.2.5 on 2022-07-20 09:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_auto_20220719_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.AddField(
            model_name='payment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 20, 14, 4, 30, 161779), verbose_name='Tarix'),
        ),
    ]
