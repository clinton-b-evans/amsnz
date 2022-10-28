# Generated by Django 4.1.1 on 2022-10-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0002_crypto_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crypto",
            name="spot_price",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=0.0, max_digits=12
            ),
        ),
    ]
