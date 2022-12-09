# Generated by Django 4.1.1 on 2022-12-06 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonalBalance",
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
                ("description", models.CharField(max_length=200)),
                (
                    "entry_type",
                    models.CharField(
                        choices=[
                            ("Asset", "Asset"),
                            ("Liability", "Liability"),
                            ("Savings", "Savings"),
                            ("Retirement Acc", "Retirement Acc"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "date",
                    models.DateField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
