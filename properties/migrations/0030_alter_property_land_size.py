# Generated by Django 4.0.1 on 2022-05-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0029_alter_property_land_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="land_size",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
