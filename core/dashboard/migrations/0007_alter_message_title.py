# Generated by Django 4.1.1 on 2022-10-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_message_created_by_remove_message_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]