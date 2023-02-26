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
            name="IndexFund",
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
                ("name", models.CharField(max_length=120)),
                ("ticker", models.CharField(blank=True, max_length=6, null=True)),
                (
                    "date",
                    models.DateField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "asset_class",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Equities", "Equities"),
                            ("Bonds", "Bonds"),
                            ("Cash & Cash Equivalents", "Cash & Cash Equivalents"),
                            ("Commodites", "Commodites"),
                            ("Diversified", "Diversified"),
                            ("Reits", "Reits"),
                            ("Other", "Other"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "fund_type",
                    models.CharField(
                        choices=[
                            ("Index Fund", "Index Fund"),
                            ("Exchange Traded Fund", "Exchange Traded Fund"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "shares",
                    models.DecimalField(
                        blank=True, decimal_places=4, default=0.0, max_digits=12
                    ),
                ),
                (
                    "share_price",
                    models.DecimalField(
                        blank=True, decimal_places=4, default=0.0, max_digits=12
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
        migrations.CreateModel(
            name="Trade",
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
                ("date", models.DateField()),
                (
                    "type",
                    models.CharField(
                        choices=[("Buy", "Buy"), ("Sell", "Sell")],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "shares",
                    models.DecimalField(
                        blank=True, decimal_places=4, default=0.0, max_digits=12
                    ),
                ),
                (
                    "share_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0.0, max_digits=12
                    ),
                ),
                (
                    "indexfund",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="market_funds.indexfund",
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
