# Generated by Django 4.0.1 on 2022-06-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commodities", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commodity",
            name="commodity_class",
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
