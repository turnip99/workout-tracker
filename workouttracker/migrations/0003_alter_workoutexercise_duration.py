# Generated by Django 5.0.6 on 2025-04-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouttracker', '0002_alter_workoutexercise_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutexercise',
            name='duration',
            field=models.DurationField(blank=True, help_text='05:00 is five minutes. 01:00:00 is one hour.', null=True),
        ),
    ]
