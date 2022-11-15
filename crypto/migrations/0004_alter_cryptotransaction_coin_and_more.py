# Generated by Django 4.1.1 on 2022-11-15 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0003_cruduser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cryptotransaction",
            name="coin",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="crypto.crypto",
            ),
        ),
        migrations.AlterField(
            model_name="cryptotransaction",
            name="transaction_type",
            field=models.CharField(
                blank=True,
                choices=[("Buy", "Buy"), ("Sell", "Sell")],
                max_length=100,
                null=True,
            ),
        ),
    ]
