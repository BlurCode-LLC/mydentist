# Generated by Django 3.2.5 on 2022-03-05 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_key_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='Telefon raqami'),
        ),
    ]
