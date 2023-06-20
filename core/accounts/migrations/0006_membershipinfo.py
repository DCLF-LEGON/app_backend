# Generated by Django 4.1.1 on 2023-06-17 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_user_otp_verified"),
    ]

    operations = [
        migrations.CreateModel(
            name="MembershipInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("program", models.CharField(blank=True, max_length=255, null=True)),
                ("department", models.CharField(blank=True, max_length=255, null=True)),
                ("level", models.CharField(blank=True, max_length=50, null=True)),
                ("hall", models.CharField(blank=True, max_length=150, null=True)),
                ("room", models.CharField(blank=True, max_length=50, null=True)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("gender", models.CharField(blank=True, max_length=8, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
