# Generated by Django 3.2.5 on 2022-04-20 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_auto_20220328_1041'),
        ('illness', '0002_auto_20220107_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fainting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(verbose_name='Qiymat')),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tavsif')),
            ],
            options={
                'verbose_name': 'Hushdan ketish ',
                'verbose_name_plural': 'Hushdan ketish',
            },
        ),
        migrations.RenameModel(
            old_name='Blood_disease',
            new_name='Breastfeeding',
        ),
        migrations.AlterModelOptions(
            name='aids',
            options={'verbose_name': 'OITS ', 'verbose_name_plural': 'OITS'},
        ),
        migrations.AlterModelOptions(
            name='alcohol',
            options={'verbose_name': "Alkogol iste'mol qilasizmi? ", 'verbose_name_plural': "Alkogol iste'mol qilasizmi?"},
        ),
        migrations.AlterModelOptions(
            name='allergy',
            options={'verbose_name': 'Allergiya ', 'verbose_name_plural': 'Allergiya'},
        ),
        migrations.AlterModelOptions(
            name='anesthesia',
            options={'verbose_name': 'Narkoz ', 'verbose_name_plural': 'Narkoz'},
        ),
        migrations.AlterModelOptions(
            name='asthma',
            options={'verbose_name': 'Bronxial astma ', 'verbose_name_plural': 'Bronxial astma'},
        ),
        migrations.AlterModelOptions(
            name='breastfeeding',
            options={'verbose_name': 'Emizasizmi? ', 'verbose_name_plural': 'Emizasizmi?'},
        ),
        migrations.AlterModelOptions(
            name='diabet',
            options={'verbose_name': 'Qand kasalligi ', 'verbose_name_plural': 'Qand kasalligi'},
        ),
        migrations.AlterModelOptions(
            name='dizziness',
            options={'verbose_name': 'Bosh aylanishi ', 'verbose_name_plural': 'Bosh aylanishi'},
        ),
        migrations.AlterModelOptions(
            name='epilepsy',
            options={'verbose_name': 'Epilepsiya (tutqanoq) ', 'verbose_name_plural': 'Epilepsiya (tutqanoq)'},
        ),
        migrations.AlterModelOptions(
            name='heart_attack',
            options={'verbose_name': "Infarkt bo'lganmisiz? ", 'verbose_name_plural': "Infarkt bo'lganmisiz?"},
        ),
        migrations.AlterModelOptions(
            name='hepatitis',
            options={'verbose_name': 'Gepatit (B yoki C) ', 'verbose_name_plural': 'Gepatit (B yoki C)'},
        ),
        migrations.AlterModelOptions(
            name='medications',
            options={'verbose_name': 'Doimiy qabul qiladigan dorilar ', 'verbose_name_plural': 'Doimiy qabul qiladigan dorilar'},
        ),
        migrations.AlterModelOptions(
            name='oncologic',
            options={'verbose_name': "Onkologik kasallik (o'sma - рак) ", 'verbose_name_plural': "Onkologik kasallik (o'sma - рак)"},
        ),
        migrations.AlterModelOptions(
            name='pregnancy',
            options={'verbose_name': 'Homiladormisiz? ', 'verbose_name_plural': 'Homiladormisiz?'},
        ),
        migrations.AlterModelOptions(
            name='pressure',
            options={'verbose_name': 'Qon bosimi ', 'verbose_name_plural': 'Qon bosimi'},
        ),
        migrations.AlterModelOptions(
            name='stroke',
            options={'verbose_name': "Insult bo'lganmisiz? ", 'verbose_name_plural': "Insult bo'lganmisiz?"},
        ),
        migrations.AlterModelOptions(
            name='tuberculosis',
            options={'verbose_name': 'Tuberkuloz ', 'verbose_name_plural': 'Tuberkuloz'},
        ),
    ]
