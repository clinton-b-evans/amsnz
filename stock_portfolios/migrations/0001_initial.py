# Generated by Django 4.1.1 on 2022-11-09 08:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("ticker", models.CharField(max_length=50, unique=True)),
                (
                    "quantity",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
                (
                    "investment",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockTransaction",
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
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("Buy", "Buy"), ("Sell", "Sell")], max_length=100
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
                (
                    "spot_price",
                    models.DecimalField(
                        blank=True, decimal_places=4, default=0.0, max_digits=12
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "coin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stock_portfolios.stock",
                    ),
                ),
            ],
        ),
    ]