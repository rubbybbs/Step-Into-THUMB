# Generated by Django 2.2.6 on 2019-11-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITHUMB', '0002_auto_20191105_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='examiners',
            field=models.ManyToManyField(to='SITHUMB.Examiner'),
        ),
    ]