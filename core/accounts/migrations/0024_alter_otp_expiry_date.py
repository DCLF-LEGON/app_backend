# Generated by Django 4.1.1 on 2022-11-01 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_otp_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 0, 0, 3, 589716)),
        ),
    ]