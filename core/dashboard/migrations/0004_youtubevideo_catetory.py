# Generated by Django 4.1.1 on 2023-05-06 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0003_youtubevideo"),
    ]

    operations = [
        migrations.AddField(
            model_name="youtubevideo",
            name="catetory",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="youtube_videos",
                to="dashboard.messagecategory",
            ),
        ),
    ]
