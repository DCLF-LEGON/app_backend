# Generated by Django 4.1.1 on 2022-12-09 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 11, 0, 5, 701941)),
        ),
    ]