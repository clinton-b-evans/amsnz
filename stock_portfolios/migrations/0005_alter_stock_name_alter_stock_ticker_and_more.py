# Generated by Django 4.1.1 on 2022-11-15 15:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stock_portfolios", "0004_stock_user_stocktransaction_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="stock",
            name="ticker",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name="stock",
            unique_together={("user", "ticker", "name")},
        ),
    ]
