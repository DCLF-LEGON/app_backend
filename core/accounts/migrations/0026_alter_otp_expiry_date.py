# Generated by Django 4.1.1 on 2022-11-14 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_alter_otp_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 14, 39, 25, 606454)),
        ),
    ]
