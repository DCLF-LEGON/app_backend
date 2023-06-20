# Generated by Django 4.1.1 on 2023-06-20 01:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_membershipinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershipinfo",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
