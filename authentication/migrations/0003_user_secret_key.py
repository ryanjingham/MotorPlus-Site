# Generated by Django 4.1.7 on 2023-04-11 23:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_remove_user_api_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="secret_key",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
