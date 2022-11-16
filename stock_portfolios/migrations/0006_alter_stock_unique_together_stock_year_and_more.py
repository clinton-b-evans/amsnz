# Generated by Django 4.1.1 on 2022-11-15 18:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stock_portfolios", "0005_alter_stock_name_alter_stock_ticker_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="stock",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="stock",
            name="year",
            field=models.CharField(default="2022", max_length=4),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="stock",
            unique_together={("user", "ticker", "name", "year")},
        ),
    ]
