# Generated by Django 4.2.21 on 2025-06-01 00:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_timesheets_pay_period_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheets',
            name='pay_period_end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='timesheets',
            name='pay_period_start',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
