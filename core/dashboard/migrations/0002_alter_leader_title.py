# Generated by Django 4.1.1 on 2022-10-16 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leader',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
