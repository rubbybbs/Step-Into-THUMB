# Generated by Django 2.2.6 on 2019-11-05 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SITHUMB', '0004_auto_20191105_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='SITHUMB.Activity'),
        ),
        migrations.AlterField(
            model_name='application',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='SITHUMB.Candidate'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='SITHUMB.Activity'),
        ),
        migrations.AlterField(
            model_name='examiner',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examiners', to='SITHUMB.Activity'),
        ),
        migrations.AlterField(
            model_name='examiner',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examiners', to='SITHUMB.Section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='SITHUMB.Activity'),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcripts', to='SITHUMB.Activity'),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcript', to='SITHUMB.Candidate'),
        ),
    ]
