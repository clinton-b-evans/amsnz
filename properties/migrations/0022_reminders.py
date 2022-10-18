# Generated by Django 4.0.1 on 2022-04-08 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0021_remove_property_loan_to_value"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reminders",
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
                ("detail", models.TextField(max_length=255)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="properties.property",
                    ),
                ),
            ],
        ),
    ]
