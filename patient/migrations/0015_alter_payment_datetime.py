# Generated by Django 3.2.5 on 2022-07-20 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0014_auto_20220720_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Tarix'),
        ),
    ]