# Generated by Django 3.2.5 on 2022-04-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentist', '0006_auto_20220323_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tajriba'),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Slug'),
        ),
    ]
