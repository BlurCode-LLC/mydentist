# Generated by Django 3.2.5 on 2022-04-20 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('illness', '0003_auto_20220420_1018'),
        ('patient', '0011_auto_20220420_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illness',
            name='fainting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='illness.fainting', verbose_name='Hushdan ketish'),
        ),
    ]
