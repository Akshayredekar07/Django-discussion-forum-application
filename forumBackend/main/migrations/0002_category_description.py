# Generated by Django 5.0.5 on 2024-07-14 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="description",
            field=models.TextField(default="description"),
        ),
    ]
