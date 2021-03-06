# Generated by Django 3.2.5 on 2022-03-10 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_tooth_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='other_illness',
            options={'verbose_name': 'Bemorning boshqa kasalligi', 'verbose_name_plural': 'Bemorning boshqa kasalliklari'},
        ),
        migrations.AlterModelOptions(
            name='process_photo',
            options={'verbose_name': 'Davolanish jarayoni', 'verbose_name_plural': 'Davolanish jarayonlari'},
        ),
        migrations.AlterField(
            model_name='tooth',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Izoh'),
        ),
    ]
