# Generated by Django 4.1.1 on 2023-01-25 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("incomestatements_property", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="propertycategory",
            unique_together={("name", "year")},
        ),
    ]