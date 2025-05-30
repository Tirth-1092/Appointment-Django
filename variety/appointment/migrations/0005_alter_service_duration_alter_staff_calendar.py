# Generated by Django 5.2 on 2025-05-08 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_appointment__end_time_alter_service_duration_and_more'),
        ('schedule', '0016_remove_calendarrelation_cal_rel_content_obj_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.DurationField(help_text='Duration of service (e.g., 0:30:00 for 30 mins)'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='calendar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='schedule.calendar'),
        ),
    ]
